[app]
title = CM Toolkit
package.name = cmtoolkit
package.domain = org.gnaneswar

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png
android.presplash_color = #FEFEFE

android.permissions =
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

# Pin python-for-android to its stable "master" branch (supports Python up to
# 3.12). Without this, buildozer was defaulting to p4a's "develop" branch,
# which requires Python 3.14 - a version pip itself has a build-isolation bug
# on right now, causing every build to fail with an unrelated-looking
# "ImportError: cannot import name 'BuildDependencyInstallError'" deep in a
# pip internals import.
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
