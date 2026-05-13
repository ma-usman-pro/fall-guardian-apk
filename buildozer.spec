[app]
title = FallGuardian
package.name = fallguardian
package.domain = org.ma_usman
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf,mp3,wav

requirements = python3, kivy==2.3.0, kivymd==1.1.1, plyer

p4a.branch = v2024.01.21
android.accept_sdk_license = True
orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION, SEND_SMS

android.enable_androidx = True
android.gradle_dependencies = com.android.support:multidex:1.0.3

android.api = 33
android.minapi = 21
log_level = 2
android.ndk = 25b
android.build_tools_version = 34.0.0
android.archs = arm64-v8a, armeabi-v7a

buildozer.use_venv = 1
p4a.env_vars = USE_OPENGL_ES2=1, USE_SDL2=1, KIVY_GRAPHICS=gles