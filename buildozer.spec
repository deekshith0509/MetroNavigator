[app]
title = Shortest Route Finder
package.name = srf
package.domain = org.deekshith
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,dm
source.main = main.py
requirements = python3,kivy,requests,matplotlib,networkx,olefile,Pillow
orientation = portrait
presplash.filename = presplash.png  
icon.filename = icon.png
fullscreen = 0
android.archs = arm64-v8a
android.release_artifact = apk
android.accept_sdk_license = True
android.api = 33
android.ndk = 25b
android.presplash_color = #FFFFFF
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# Versioning
version = 0.2

# Debug mode
debug = 1

[buildozer]
log_level = 2
warn_on_root = 1

android.allow_backup = True
android.logcat = True