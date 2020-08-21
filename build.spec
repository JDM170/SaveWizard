# -*- mode: python ; coding: utf-8 -*-

app = Analysis(
    ['init_main_program.py'],
    pathex=['.'],
    datas=[
        ('configs/ats', 'configs/ats'),
        ('configs/ets2', 'configs/ets2')
    ]
)

app_pyz = PYZ(app.pure, app.zipped_data)

app_exe = EXE(
    app_pyz,
    app.scripts,
    [],
    exclude_binaries=True,
    name='SaveWizard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    console=False
)
app_coll = COLLECT(
    app_exe,
    app.binaries,
    app.zipfiles,
    app.datas,
    strip=False,
    name='app_build'
)

