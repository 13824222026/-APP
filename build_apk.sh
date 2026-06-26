#!/bin/bash
# ================================================================
# 全球实时行情 APP - APK 构建脚本
# 运行环境: Ubuntu/Debian Linux 或 WSL2
# ================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=========================================="
echo "  全球实时行情 APP - APK 构建脚本"
echo "=========================================="
echo "工作目录: $SCRIPT_DIR"
echo ""

# 检查是否安装了 buildozer
if ! command -v buildozer &> /dev/null; then
    echo "[1/4] 安装 buildozer 和依赖..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq \
        python3-pip python3-dev python3-venv \
        git zip unzip openjdk-17-jdk \
        autoconf libtool pkg-config \
        zlib1g-dev libncurses5-dev \
        libncursesw5-dev libtinfo5 \
        cmake libffi-dev libssl-dev \
        wget curl 2>&1 | tail -3

    pip3 install --user --upgrade buildozer cython
    export PATH=$PATH:$HOME/.local/bin
fi

echo "[2/4] 清理旧构建..."
cd "$SCRIPT_DIR"
rm -rf .buildozer bin 2>/dev/null
mkdir -p bin

echo "[3/4] 构建 APK..."
echo "  (首次构建需要下载 SDK/NDK，约 10-30 分钟)"
echo ""

buildozer android debug

echo ""
echo "[4/4] 清理中间文件..."
# 保留 APK，清理构建缓存
APK_FILE=$(ls bin/*.apk 2>/dev/null | head -1)
if [ -f "$APK_FILE" ]; then
    SIZE=$(du -h "$APK_FILE" | cut -f1)
    echo "=========================================="
    echo "  ✓ 构建成功！"
    echo "  APK 文件: $APK_FILE"
    echo "  大小: $SIZE"
    echo "=========================================="
    echo ""
    echo "安装到手机:"
    echo "  adb install $APK_FILE"
    echo "  或直接发送 APK 文件到手机安装"
else
    echo "  ✗ 构建失败，请检查 buildozer.spec 配置"
    exit 1
fi
