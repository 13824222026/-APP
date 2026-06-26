#!/bin/bash
# ============================================================
# 全球实时行情APP - Linux一键APK构建脚本
# 适用于: Ubuntu/Debian (WSL, 原生Linux, 云服务器)
# ============================================================
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}  📊 全球实时行情APP - APK构建${NC}"
echo -e "${BLUE}====================================================${NC}"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 步骤1: 安装系统依赖
echo -e "\n${YELLOW}[1/5] 安装系统依赖...${NC}"
sudo apt-get update -qq
sudo apt-get install -y -qq \
    git zip unzip openjdk-17-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    cmake libffi-dev libssl-dev \
    wget curl 2>&1 | tail -2

# 步骤2: 设置JAVA_HOME
echo -e "\n${YELLOW}[2/5] 设置JAVA_HOME...${NC}"
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
echo "JAVA_HOME=$JAVA_HOME"

# 步骤3: 安装Python依赖
echo -e "\n${YELLOW}[3/5] 安装Python依赖...${NC}"
pip install --upgrade pip setuptools wheel 2>&1 | tail -1
pip install buildozer cython 2>&1 | tail -3

# 步骤4: 检查项目文件
echo -e "\n${YELLOW}[4/5] 检查项目文件...${NC}"
REQUIRED_FILES=("main.py" "price_fetcher.py" "buildozer.spec")
MISSING=0
for f in "${REQUIRED_FILES[@]}"; do
    if [ -f "$f" ]; then
        echo "  ✅ $f"
    else
        echo "  ❌ $f (缺失!)"
        MISSING=1
    fi
done

if [ $MISSING -eq 1 ]; then
    echo -e "\n${RED}❌ 项目文件缺失，请确认在正确的目录运行${NC}"
    exit 1
fi

# 步骤5: 构建APK
echo -e "\n${YELLOW}[5/5] 开始构建APK (首次约15-30分钟)...${NC}"
echo -e "${YELLOW}  构建过程中将自动下载SDK/NDK...${NC}"
echo ""

BUILD_START=$(date +%s)
buildozer android debug 2>&1
BUILD_END=$(date +%s)
BUILD_TIME=$((BUILD_END - BUILD_START))

# 检查结果
APK_FILES=$(ls bin/*.apk 2>/dev/null || true)
if [ -n "$APK_FILES" ]; then
    for apk in $APK_FILES; do
        SIZE=$(stat --printf="%s" "$apk")
        SIZE_MB=$(echo "scale=1; $SIZE / 1048576" | bc)
        echo -e "\n${GREEN}✅ 构建成功！${NC}"
        echo -e "${GREEN}  APK路径: $(realpath "$apk")${NC}"
        echo -e "${GREEN}  文件大小: ${SIZE_MB}MB${NC}"
        echo -e "${GREEN}  构建用时: ${BUILD_TIME}秒${NC}"
    done
else
    echo -e "\n${RED}❌ 未找到APK文件，构建可能失败${NC}"
    echo -e "${RED}  请检查上方日志中的错误信息${NC}"
    exit 1
fi

echo -e "\n${BLUE}====================================================${NC}"
echo -e "${GREEN}  🎉 APK编译完成！${NC}"
echo -e "${BLUE}====================================================${NC}"
