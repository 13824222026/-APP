"""
实时行情APP - Kivy/KivyMD 主界面
支持：黄金、白银、石油、美元指数、美元/人民币
Material Design 风格，适配安卓
"""
import json
import threading
import time
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.utils import platform, get_color_from_hex
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import (
    StringProperty, NumericProperty, BooleanProperty,
    ObjectProperty, DictProperty, ListProperty,
)
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, CardTransition
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation
from kivy.core.window import Window

from price_fetcher import get_all_prices

# ── Color Palette ──────────────────────────────────────────
BLACK = (0.05, 0.05, 0.07, 1)
DARK_CARD = (0.09, 0.09, 0.13, 1)
DARK_CARD_HOVER = (0.13, 0.13, 0.18, 1)
ACCENT_GREEN = (0.0, 0.78, 0.33, 1)
ACCENT_RED = (0.96, 0.26, 0.21, 1)
ACCENT_GOLD = (1.0, 0.84, 0.0, 1)
ACCENT_SILVER = (0.75, 0.75, 0.80, 1)
ACCENT_OIL = (0.0, 0.60, 0.86, 1)
ACCENT_BLUE = (0.22, 0.46, 1.0, 1)
WHITE = (0.95, 0.95, 0.98, 1)
GRAY_TEXT = (0.55, 0.55, 0.60, 1)

# ── Asset Config ───────────────────────────────────────────
ASSETS = [
    {"key": "gold",   "name": "黄金",   "symbol": "XAU/USD",  "unit": "美元/盎司", "icon": "🥇", "color": ACCENT_GOLD},
    {"key": "silver", "name": "白银",   "symbol": "XAG/USD",  "unit": "美元/盎司", "icon": "🥈", "color": ACCENT_SILVER},
    {"key": "oil",    "name": "原油",   "symbol": "WTI",      "unit": "美元/桶",   "icon": "🛢️", "color": ACCENT_OIL},
    {"key": "dxy",    "name": "美元指数", "symbol": "DXY",    "unit": "",          "icon": "💵", "color": ACCENT_BLUE},
    {"key": "usdcny", "name": "美元/人民币", "symbol": "USD/CNY", "unit": "",      "icon": "🇨🇳", "color": (0.85, 0.15, 0.10, 1)},
]


class PriceCard(RelativeLayout):
    """A card widget displaying a single asset price."""
    asset_key = StringProperty("")
    asset_name = StringProperty("")
    symbol = StringProperty("")
    unit = StringProperty("")
    icon = StringProperty("")
    card_color = ListProperty(DARK_CARD)
    price_text = StringProperty("---")
    change_text = StringProperty("")
    change_color = ListProperty(GRAY_TEXT)
    last_update = StringProperty("")

    def __init__(self, asset_config, **kwargs):
        super().__init__(**kwargs)
        self.asset_key = asset_config["key"]
        self.asset_name = asset_config["name"]
        self.symbol = asset_config["symbol"]
        self.unit = asset_config["unit"]
        self.icon = asset_config["icon"]
        self.card_color = DARK_CARD
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        """Redraw rounded rectangle on resize."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.card_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])

    def update_price(self, price, change):
        """Update display with new price data."""
        if self.asset_key == "usdcny":
            self.price_text = f"{price:.4f}"
        else:
            self.price_text = f"{price:.2f}"

        if change >= 0:
            self.change_text = f"▲ +{change:.2f}%"
            self.change_color = ACCENT_GREEN
        else:
            self.change_text = f"▼ {change:.2f}%"
            self.change_color = ACCENT_RED

        now = datetime.now()
        self.last_update = now.strftime("%H:%M:%S")


class MarketScreen(Screen):
    """Main screen displaying all asset prices."""
    data_loaded = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prices = {}
        self.cards = {}
        self._build_ui()
        self._start_updating()

    def _build_ui(self):
        """Build the main user interface."""
        # Main layout
        main = FloatLayout()

        # Background color
        with main.canvas.before:
            Color(*BLACK)
            RoundedRectangle(pos=main.pos, size=main.size, radius=[0])

        # Title bar
        title_bar = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(80),
            pos_hint={"top": 1},
            padding=[dp(20), dp(12), dp(20), dp(4)],
        )
        with title_bar.canvas.before:
            Color(*BLACK)
            RoundedRectangle(pos=title_bar.pos, size=title_bar.size, radius=[0])

        title = Label(
            text="📊 全球实时行情",
            font_size=sp(22),
            bold=True,
            color=WHITE,
            halign="left",
            size_hint_x=1,
            height=dp(32),
            text_size=(Window.width - dp(40), None),
        )
        title.bind(text_size=title.setter("size"))
        title_bar.add_widget(title)

        subtitle = Label(
            text="数据来自公开API · 每15秒自动刷新",
            font_size=sp(12),
            color=GRAY_TEXT,
            halign="left",
            size_hint_x=1,
            height=dp(20),
            text_size=(Window.width - dp(40), None),
        )
        subtitle.bind(text_size=subtitle.setter("size"))
        title_bar.add_widget(subtitle)
        main.add_widget(title_bar)

        # Scrollable card area
        scroll = ScrollView(
            pos_hint={"top": 0.88},
            size_hint=(1, 0.88),
            bar_width=dp(2),
            bar_color=GRAY_TEXT,
        )

        card_grid = GridLayout(
            cols=1,
            spacing=dp(12),
            padding=[dp(16), dp(8), dp(16), dp(24)],
            size_hint_y=None,
        )
        card_grid.bind(minimum_height=card_grid.setter("height"))

        for asset in ASSETS:
            card = PriceCard(asset)
            card.size_hint_y = None
            card.height = dp(110)
            card_grid.add_widget(card)
            self.cards[asset["key"]] = card

        scroll.add_widget(card_grid)
        main.add_widget(scroll)

        # Refresh button at bottom
        refresh_btn = Button(
            text="🔄 刷新",
            size_hint=(None, None),
            size=(dp(120), dp(44)),
            pos_hint={"center_x": 0.5, "y": dp(8)},
            background_normal="",
            background_color=(0.15, 0.15, 0.22, 1),
            color=WHITE,
            font_size=sp(14),
        )
        with refresh_btn.canvas.before:
            Color(0.15, 0.15, 0.22, 1)
            RoundedRectangle(pos=refresh_btn.pos, size=refresh_btn.size, radius=[dp(22)])
        refresh_btn.bind(on_release=lambda btn: self._refresh_now())
        main.add_widget(refresh_btn)

        self.add_widget(main)

    def _start_updating(self):
        """Start periodic price updates."""
        self._refresh_now()
        Clock.schedule_interval(lambda dt: self._refresh_now(), 15)

    def _refresh_now(self):
        """Fetch prices in a background thread."""
        thread = threading.Thread(target=self._fetch_worker, daemon=True)
        thread.start()

    def _fetch_worker(self):
        """Background worker to fetch prices."""
        try:
            data = get_all_prices()
            self.data_loaded = True
            # Update UI on main thread
            Clock.schedule_once(lambda dt: self._update_cards(data))
        except Exception:
            pass

    def _update_cards(self, data):
        """Update all cards with fetched data."""
        for asset in ASSETS:
            key = asset["key"]
            card = self.cards.get(key)
            if card and key in data:
                price, change = data[key]
                card.update_price(price, change)


class MarketApp(App):
    """Main application class."""

    def build(self):
        """Build the application."""
        if platform != "android":
            Window.size = (400, 800)
        self.title = "全球实时行情"

        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        sm.add_widget(MarketScreen(name="market"))
        return sm


if __name__ == "__main__":
    MarketApp().run()
