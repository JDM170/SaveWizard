#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import argv, exit
from PyQt5.QtWidgets import QApplication
from module_main.script import MainWindow

if __name__ == '__main__':
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
