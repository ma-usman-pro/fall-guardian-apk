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

# ── THE FIX: Added json, ttf, mp3, wav so Android packages them ──
source.include_exts = py,png,jpg,kv,atlas,json,ttf,mp3,wav

# ── THE FIX: Locked KivyMD to 1.1.1 to prevent syntax crash ──
requirements = python3, kivy==2.3.0, kivymd==1.1.1, plyer

# (str) python-for-android branch to use, defaults to master
p4a.branch = v2024.01.21

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
android.gradle_dependencies = com.android.support:multidex:1.0.3

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android build tools version to use
android.build_tools_version = 34.0.0

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) use buildozer virtualenv
buildozer.use_venv = 1

# (list) python-for-android environment variables
p4a.env_vars = USE_OPENGL_ES2=1, USE_SDL2=1, KIVY_GRAPHICS=gles