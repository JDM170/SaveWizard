#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from sys import argv, exit
    from PyQt5.QtWidgets import QApplication
    from main.script import MainWindow
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
