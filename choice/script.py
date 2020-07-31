#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox
from ast import literal_eval
from .form import Ui_Choice
from main.script import MainWindow
from parsing.script import check_remote_hashes, update_configs
from util import update_config_name


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
        try:
            with open(update_config_name) as f:
                remember_data = literal_eval(f.read())
        except FileNotFoundError:
            with open(update_config_name, "w") as f:
                f.write(str(remember_data))

        upd_list = check_remote_hashes()
        if upd_list and len(upd_list) > 0:
            answer = remember_data.get("answer_updates")
            if answer:
                box = QMessageBox(QMessageBox.Information, "Info",
                                  "Some configs get updated, do you want update your local configs?")
                box.addButton("Yes", QMessageBox.YesRole)  # 0
                box.addButton("Yes, remember that", QMessageBox.YesRole)  # 1
                box.addButton("No", QMessageBox.NoRole)  # 2
                box.addButton("No, remember that", QMessageBox.NoRole)  # 3
                update_configs(box.exec(), upd_list)
                return
            upd_on_start = remember_data.get("update_on_start")
            if upd_on_start:
                update_configs(1, upd_list)

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
