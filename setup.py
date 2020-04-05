#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

executables = [Executable('__init__.py', targetName='SaveWizard.exe', base='Win32GUI')]
excludes = ['email', 'html', 'http', 'logging', 'pydoc_data', 'unittest', 'urllib', 'xml', 'tempfile', 'select', 'pwd',
            'datetime', 'shlex', 'shutil', 'socket', 'platform', 'webbrowser', 'pydoc', 'selectors', 'tty', 'inspect',
            'doctest', 'plistlib', 'calendar', 'subprocess', 'copy', 'bz2', 'stringprep', 'posixpath', '_strptime',
            'dummy_threading']
zip_include_packages = ['collections', 'encodings', 'importlib', 'json', 'hashlib', 'PyQt5', 'sip', 'main', 'second']
include_files = ['SII_Decrypt.exe', 'ats_configs', 'ets2_configs']
options = {
    'build_exe': {
        'excludes': excludes,
        'include_msvcr': True,
        'build_exe': 'stable_build',
        'include_files': include_files,
        'zip_include_packages': zip_include_packages,
    }
}

setup(
    name='SaveWizard',
    version='1.1',
    description='For editing ETS2 sii files',
    executables=executables,
    options=options,
    requires=['PyQt5']
)
