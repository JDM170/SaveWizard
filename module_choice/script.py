#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox
from ast import literal_eval
from os.path import isfile
from .form import Ui_Choice
from module_main.script import MainWindow
from module_parsing.script import check_remote_hashes, update_configs
from statics import update_config_name


class ChoiceWindow(QDialog, Ui_Choice):
    def __init__(self, parent=None):
        # Setup UI
        QDialog.__init__(self, parent, flags=Qt.Window)
        Ui_Choice.__init__(self)
        self.ui = Ui_Choice()
        self.ui.setupUi(self)

        self.ui.ats_button.clicked.connect(self.button_clicked)
        self.ui.ets2_button.clicked.connect(self.button_clicked)

        remember_data = {"answer_updates": True, "update_on_start": False}
        if isfile(update_config_name):
            with open(update_config_name, "r") as f:
                remember_data = literal_eval(f.read())

        upd_list = check_remote_hashes()
        if upd_list and len(upd_list) > 0:
            if remember_data.get("update_on_start"):
                update_configs(upd_list)
                return
            if remember_data.get("answer_updates"):
                box = QMessageBox(QMessageBox.Information, "Info",
                                  "Some configs have been updated. Do you want to update the local configs?")
                box.addButton("Yes", QMessageBox.YesRole)  # 0
                box.addButton("Yes, remember that", QMessageBox.YesRole)  # 1
                box.addButton("No", QMessageBox.NoRole)  # 2
                box.addButton("No, remember that", QMessageBox.NoRole)  # 3
                update_configs(upd_list, box.exec())

    def button_clicked(self):
        sender = self.sender()
        if sender == self.ui.ats_button:
            selected = "ats"
        elif sender == self.ui.ets2_button:
            selected = "ets2"
        else:
            return
        self.close()
        win = MainWindow(selected)
        win.exec()
