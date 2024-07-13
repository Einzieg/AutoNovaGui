# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('static', 'static')],
    hiddenimports=['cv2', 'pygetwindow', 'pyautogui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='AutoNovaGui',
    icon=['./static/ico/auto.icns'],
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AutoNovaGui',
)
app = BUNDLE(
    coll,
    name='AutoNovaGui.app',
    icon='./static/ico/auto.icns',
    bundle_identifier=None
)
