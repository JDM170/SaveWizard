#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import platform
from cx_Freeze import setup, Executable

base = None
if platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('init_main_program.py', target_name='SaveWizard.exe', base=base),
    Executable('init_config_editor.py', target_name='SaveWizard_Config_Editor.exe', base=base)
]

excludes = ['html', 'pydoc_data', 'unittest', 'xml', 'pwd', 'shlex', 'platform', 'webbrowser', 'pydoc', 'tty',
            'inspect', 'doctest', 'plistlib', 'subprocess', 'bz2', '_strptime', 'dummy_threading']

includes = ['pkgutil', 'enum', 'queue']

zip_include_packages = [
    # Stock modules
    'collections', 'encodings', 'importlib', 'json', 'hashlib', 'selectors', 'select', 'http', 'email', 'datetime',
    'calendar', 'urllib', 'posixpath', 'tempfile', 'shutil', 'copy', 'stringprep', 'socket', 'ast',
    # PyQt5
    'PyQt5',
    # Modules for parsing cfg's
    'requests', 'logging', 'certifi', 'chardet', 'idna', 'urllib3',
    # Self-written modules
    'module_parsing', 'module_choice', 'module_main', 'module_second', 'module_config_editor'
]

include_files = [
    'dlls/imageformats',
    'dlls/platforms',
    'dlls/styles',
    'SII_Decrypt.exe',
    ('configs/ats', 'configs/ats'),
    ('configs/ets2', 'configs/ets2')
]

options = {
    'build_exe': {
        'excludes': excludes,
        'includes': includes,
        'include_msvcr': True,
        'build_exe': 'prog_build',
        'include_files': include_files,
        'zip_include_packages': zip_include_packages,
    }
}

setup(
    name='SaveWizard',
    version='1.3',
    description='For editing ETS2 sii files',
    executables=executables,
    options=options,
    requires=['PyQt5', 'requests'],
)
