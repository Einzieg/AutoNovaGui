# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# 获取项目目录的绝对路径
project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
static_dir = os.path.join(project_dir, 'static')
icon_path = os.path.join(static_dir, 'ico', 'auto.ico')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(static_dir, 'static')],
    hiddenimports=['cv2','pygetwindow','pyautogui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AutoNovaGui-Base-2.2',
    icon=icon_path,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
