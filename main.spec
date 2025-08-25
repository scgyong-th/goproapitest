# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

a = Analysis(
    ['runner_ui/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('runner_ui/res/main.html', 'runner_ui/res'),
        ('runner_ui/res/main.css', 'runner_ui/res'),
        ('runner_ui/res/ext/bootstrap.min.css', 'runner_ui/res/ext'),
        ('runner_ui/res/ext/jquery-3.7.1.min.js', 'runner_ui/res/ext'),
        ('testrunner/tests', 'testrunner/tests'),
        ('testrunner/camera', 'testrunner/camera'),
        ('testrunner/proto', 'testrunner/proto'),
    ] + collect_data_files('pytest_html', includes=['resources/*']),
    hiddenimports=(
      collect_submodules('construct') + 
      collect_submodules('requests') + 
      collect_submodules('google.protobuf') + 
      collect_submodules('pytest_html') + 
      collect_submodules('pytest_metadata') + 
      collect_submodules('camera') + 
      collect_submodules('proto')
    ),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['runner_ui\\assets\\icons\\dashcam_tester.ico'],
)
