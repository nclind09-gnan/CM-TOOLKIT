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

# Pin python-for-android to its last stable PyPI-released version (not a
# branch name). "master" was expected to stay on Python <=3.12, but as of
# this build it's also pulling in Python 3.14 requirements - p4a's "develop"
# branch had a long backlog of unmerged changes (including 3.14 support) that
# appear to have since landed on master too. Pinning an exact old release tag
# avoids that entirely, regardless of what master does going forward.
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1warn_on_root = 1
