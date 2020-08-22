# -*- mode: python ; coding: utf-8 -*-

app = Analysis(
    ['init_main_program.py'],
    pathex=['.'],
    datas=[
        ('configs/ats', 'configs/ats'),
        ('configs/ets2', 'configs/ets2')
    ]
)
cfg = Analysis(
    ['init_config_editor.py'],
    pathex=['.']
)

MERGE(
    (app, 'SaveWizard', 'SaveWizard'),
    (cfg, 'SaveWizard_Config_Editor', 'SaveWizard_Config_Editor')
)

app_pyz = PYZ(app.pure, app.zipped_data)
cfg_pyz = PYZ(cfg.pure, cfg.zipped_data)

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

cfg_exe = EXE(
    cfg_pyz,
    cfg.scripts,
    [],
    exclude_binaries=True,
    name='SaveWizard_Config_Editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    console=False
)
cfg_coll = COLLECT(
    cfg_exe,
    cfg.binaries,
    cfg.zipfiles,
    cfg.datas,
    strip=False,
    name='cfg_build'
)
