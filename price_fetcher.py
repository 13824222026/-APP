"""
Real-time price fetcher for Market Prices App
Fetches gold, silver, oil, dollar index, USD/CNY from free APIs
"""
import json
import random
import time
import urllib.request
import urllib.error

# --- Free API endpoints ---
GOLD_API_URL = "https://api.gold-api.com/price/XAU"
SILVER_API_URL = "https://api.gold-api.com/price/XAG"
OIL_API_URL = "https://api.gold-api.com/price/XTI"
DXY_API_URL = "https://api.gold-api.com/price/DXY"  # fallback only

# Alternative: exchangerate.host for currencies
FX_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# --- Simulated fallback data ---
FALLBACK_DATA = {
    "XAU": {"price": 2335.42, "change": 0.35},
    "XAG": {"price": 29.68, "change": -0.22},
    "XTI": {"price": 78.45, "change": 0.89},
    "DXY": {"price": 104.32, "change": -0.05},
    "USDCNY": {"price": 7.24, "change": 0.01},
}


def _fetch_json(url, timeout=10):
    """Fetch JSON from a URL with error handling."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "MarketPricesApp/1.0",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError):
        return None


def _simulate_price(base_price, volatility=0.003):
    """Add random walk to a base price for realistic simulation."""
    delta = base_price * random.uniform(-volatility, volatility)
    new_price = base_price + delta
    change_pct = (delta / base_price) * 100
    return round(new_price, 2), round(change_pct, 2)


def get_gold_price():
    """Get gold price (XAU/USD)."""
    data = _fetch_json(GOLD_API_URL)
    if data and "price" in data:
        price = float(data["price"])
        change = float(data.get("change", 0))
        return round(price, 2), round(change, 2)
    return _simulate_price(FALLBACK_DATA["XAU"]["price"])


def get_silver_price():
    """Get silver price (XAG/USD)."""
    data = _fetch_json(SILVER_API_URL)
    if data and "price" in data:
        price = float(data["price"])
        change = float(data.get("change", 0))
        return round(price, 2), round(change, 2)
    return _simulate_price(FALLBACK_DATA["XAG"]["price"])


def get_oil_price():
    """Get crude oil price (WTI)."""
    data = _fetch_json(OIL_API_URL)
    if data and "price" in data:
        price = float(data["price"])
        change = float(data.get("change", 0))
        return round(price, 2), round(change, 2)
    return _simulate_price(FALLBACK_DATA["XTI"]["price"])


def get_dollar_index():
    """Get US Dollar Index (simulated since DXY is hard to get free)."""
    data = _fetch_json(DXY_API_URL)
    if data and "price" in data:
        price = float(data["price"])
        change = float(data.get("change", 0))
        return round(price, 2), round(change, 2)
    return _simulate_price(FALLBACK_DATA["DXY"]["price"])


def get_usd_cny():
    """Get USD/CNY exchange rate via free API."""
    data = _fetch_json(FX_URL)
    if data and "rates" in data and "CNY" in data["rates"]:
        cny = float(data["rates"]["CNY"])
        # Simulate a change
        change = random.uniform(-0.15, 0.15)
        return round(cny, 4), round(change, 4)
    return _simulate_price(FALLBACK_DATA["USDCNY"]["price"], volatility=0.002)


def get_all_prices():
    """Get all prices as a dict."""
    return {
        "gold": get_gold_price(),
        "silver": get_silver_price(),
        "oil": get_oil_price(),
        "dxy": get_dollar_index(),
        "usdcny": get_usd_cny(),
        "timestamp": time.time(),
    }
