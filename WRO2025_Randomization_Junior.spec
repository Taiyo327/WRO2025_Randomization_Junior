# -*- mode: python ; coding: utf-8 -*-

import os
import glob

a = Analysis(
    ['WRO2025_Randomization_Junior.py'],
    pathex=['..\\'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

for filepath in glob.glob('img/*'):
    if os.path.isfile(filepath):
        a.datas += [(os.path.join('img', os.path.basename(filepath)), filepath, 'DATA')]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WRO2025_Randomization_Junior',
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
