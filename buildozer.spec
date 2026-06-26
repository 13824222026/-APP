[app]

# (str) Title of your application
title = 全球实时行情

# (str) Package name
package.name = marketprices

# (str) Package domain (needed for android/ios packaging)
package.domain = org.nousresearch

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let everything)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions
source.include_patterns = *.py

# (list) List of exclusions
source.exclude_patterns = build,__pycache__,.git

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (str) Application icon (filepath)
icon.filename = icon-192.png

# (str) Presplash (loading screen)
# presplash.filename = presplash.png

# (str) Orientation (one of portrait, landscape, portrait-reverse, landscape-reverse, sensor)
orientation = portrait

# (list) Supported orientations
# orientations = portrait, landscape

# (list) Permissions for Android
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Android API level
android.api = 34

# (int) Android minimum API
android.minapi = 21

# (int) Android SDK version
# android.sdk = 24

# (str) Android NDK version
# android.ndk = 23b

# (bool) If True, then skip trying to update the Android SDK
android.accept_sdk_license = True

# (str) A directory that contains libraries to use
# android.library_references =

# (str) Android private storage path (empty = use default)
# android.private_storage_path =

# (list) Java dependencies
# android.add_jars = foo.jar,bar.jar

# (list) Python dependencies
requirements = python3,kivy==2.3.1,kivymd==1.2.0,requests

# (str) Custom Android source code
# android.src =

# (str) Presplash background color (CSS color)
# presplash.color = #0d1117

# (str) Supported Android architectures
android.archs = arm64-v8a

# (str) Android logcat filter
# android.logcat_filters =

# (bool) Copy library instead of making a libs directory
# android.copy_libs = True

# (str) Android entry point (default: main.py)
# android.entrypoint = main.py

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 1

# (str) Path to build artifact storage, must be writeable
build_dir = ./.buildozer

# (str) Path to build output (APKs here)
bin_dir = ./bin

# (str) Android SDK directory
# android.sdk_path =

# (str) Android NDK directory
# android.ndk_path =

# (str) Android ANT directory
# android.ant_path =

# (bool) If True, then accept all licenses
android.accept_sdk_license = True
