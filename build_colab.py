"""
全球实时行情APP - Google Colab 一键 APK 构建
使用方法: 
  1. 打开 https://colab.research.google.com
  2. 新建笔记本，粘贴本文件内容
  3. 点击运行
"""

import os
import sys
import subprocess
from pathlib import Path

# ============================================================
PROJECT_DIR = "/content/marketprices"
# ============================================================

print("=" * 50)
print("📊 全球实时行情APP - APK构建")
print("=" * 50)

# 步骤1: 安装依赖
print("\n[1/4] 安装依赖...")
subprocess.run(["pip", "install", "-q", "kivy", "kivymd", "buildozer", "cython"],
               capture_output=False)

# 步骤2: 安装系统依赖
print("[2/4] 安装系统依赖...")
subprocess.run(["apt-get", "update", "-qq"], capture_output=True)
subprocess.run([
    "apt-get", "install", "-y", "-qq",
    "git", "zip", "unzip", "openjdk-17-jdk",
    "autoconf", "libtool", "pkg-config",
    "zlib1g-dev", "libncurses5-dev",
    "cmake", "libffi-dev", "libssl-dev",
], capture_output=True)

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

# 步骤3: 上传项目文件
print("[3/4] 上传项目文件...")
# 你需要在此代码单元格之前运行文件上传:
# from google.colab import files
# uploaded = files.upload()
# 然后将所有文件解压到 /content/marketprices/

# 或者从GitHub克隆
if not os.path.exists(PROJECT_DIR):
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print("  请上传项目文件到 /content/marketprices/")
    print("  需要的文件: main.py, price_fetcher.py, buildozer.spec")
    from google.colab import files
    uploaded = files.upload()
    # 解压zip
    for fname in uploaded:
        if fname.endswith('.zip'):
            import zipfile
            with zipfile.ZipFile(fname, 'r') as zf:
                zf.extractall(PROJECT_DIR)
else:
    print(f"  项目已存在: {PROJECT_DIR}")

# 步骤4: 构建APK
print("\n[4/4] 构建APK (约15-30分钟)...")
print("  首次构建需要下载 SDK/NDK...")
print("")

os.chdir(PROJECT_DIR)
result = subprocess.run(
    ["buildozer", "android", "debug"],
    capture_output=True, text=True, timeout=7200
)

# 打印最后部分
lines = result.stdout.split('\n')
print('\n'.join(lines[-30:]))
if result.stderr:
    print("STDERR:", result.stderr[-500:])

# 查找APK
apk_files = list(Path(PROJECT_DIR).glob("bin/*.apk"))
if apk_files:
    apk = apk_files[0]
    size = os.path.getsize(apk) / (1024 * 1024)
    print(f"\n✅ 构建成功！")
    print(f"APK: {apk}")
    print(f"大小: {size:.1f} MB")

    # 下载
    from google.colab import files
    files.download(str(apk))
else:
    print("\n❌ 构建失败，请检查上方日志")
