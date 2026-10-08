[app]

title = RDX AI Studio
package.name = rdxaistudio
package.domain = org.rdx
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt
version = 1.0.0
requirements = python3,kivy,requests,certifi
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 35
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
source.exclude_dirs = bin,.buildozer,.git,__pycache__

[buildozer]
log_level = 2
warn_on_root = 1
