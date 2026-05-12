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

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# CRITICAL: We lock Cython to 0.29.33 to fix the 'exit code 1' error
# (list) Application requirements
requirements = python3, kivy==2.3.0, kivymd, plyer, twilio, cython==0.29.33

# (bool) Auto accept Android SDK licenses
android.accept_sdk_license = True

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) use buildozer virtualenv
buildozer.use_venv = 1