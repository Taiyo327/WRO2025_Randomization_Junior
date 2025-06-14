# -*- mode: python ; coding: utf-8 -*-


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

a.datas += [('Junior_map.png', '.\\Junior_map.png', 'DATA'),
            ('green.png', '.\\green.png', 'DATA'),
            ('red.png', '.\\red.png', 'DATA'),
            ('yellow.png', '.\\yellow.png', 'DATA'),
            ('white.png', '.\\white.png', 'DATA')]

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
