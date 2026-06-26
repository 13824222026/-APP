# 全球实时行情APP 📊

Kivy + KivyMD 编写的安卓行情APP，支持：
- 🥇 黄金 (XAU/USD)
- 🥈 白银 (XAG/USD)
- 🛢️ 原油 (WTI)
- 💵 美元指数
- 🇨🇳 美元/人民币 (USD/CNY)

## 构建APK

### 方法1: GitHub Actions (推荐 - 无需本地Linux)

1. 将本项目推送到 GitHub 仓库
2. 打开 GitHub 仓库页面，点击 `Actions` 标签
3. 在左侧选择 `Build Android APK`
4. 点击 `Run workflow` -> `Run workflow`
5. 等待约15-30分钟，构建完成后下载APK

### 方法2: WSL (Windows用户)

1. 安装 WSL: `wsl --install -d Ubuntu`
2. 启动 WSL: `wsl`
3. 进入项目目录: `cd /mnt/c/Users/你的用户名/Desktop/产品开发/实时行情APP`
4. 运行构建脚本: `bash build_linux.sh`

### 方法3: Google Colab

1. 打开 https://colab.research.google.com
2. 新建笔记本，运行以下代码上传并构建

### 方法4: 原生Linux / VPS

```bash
chmod +x build_linux.sh
./build_linux.sh
```

## 项目结构

```
实时行情APP/
├── main.py              # 主程序入口
├── price_fetcher.py     # 数据获取模块
├── buildozer.spec       # Buildozer配置
├── build_linux.sh       # Linux一键构建脚本
├── build_colab.py       # Colab构建脚本
├── .github/workflows/   # GitHub Actions配置
│   └── build-apk.yml
└── APK获取指南.txt       # 使用说明
```

## APK下载

构建完成后，APK文件位于 `bin/` 目录下，文件名类似 `marketprices-1.0.0-*-debug.apk`。
