[app]
# (str) Title of your application
title = FallGuardian

# (str) Package name
package.name = fallguardian

# (str) Package domain (needed for android packaging)
package.domain = org.ma_usman

# (str) Application versioning
version = 1.0.0

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# Using kivy==master is required for Python 3.13+ compatibility
requirements = python3, kivy==2.3.0, kivymd, plyer

# (bool) Auto accept Android SDK licenses
android.accept_sdk_license = True

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions needed for GPS and internet alerts
android.permissions = INTERNET, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION

# ─── CRITICAL GRADLE SETTINGS ───
# (bool) Enable AndroidX support (Required for modern KivyMD)
android.enable_androidx = True

# (list) Gradle dependencies (Required to fix the 64k method limit / Gradle error)
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (str) Android NDK version to use
android.ndk = 26b

# (str) Android build tools version to use
android.build_tools_version = 34.0.0

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) use buildozer virtualenv
buildozer.use_venv = 1

