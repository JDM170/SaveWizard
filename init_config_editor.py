#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import argv, exit
from PyQt5.QtWidgets import QApplication
from config_editor.script import EditorWindow

if __name__ == '__main__':
    app = QApplication(argv)
    win = EditorWindow()
    win.show()
    exit(app.exec())
