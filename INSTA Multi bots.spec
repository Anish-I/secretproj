# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['The_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('The_gui.py', '.'), ('captcha_solver_selen.py', '.'), ('get_customers.py', '.'), ('login_handling_for_tester.py', '.'), ('login_handling.py', '.'), ('process_the_xlsx.py', '.'), ('start1_with_last_mod.py', '.'), ('needs', 'needs'), ('extentions', 'extentions'), ('cookies', 'cookies'), ('logo.png', '.')],
    hiddenimports=[''],
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
    name='INSTA Multi bots',
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
    icon=['logo.png'],
)
