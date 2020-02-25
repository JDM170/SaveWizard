#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from .form import Ui_MainWindow
from util import *
from dataIO import dataIO


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        from PyQt5.QtCore import Qt
        QMainWindow.__init__(self, parent, flags=Qt.Window)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_path = ""
        self.old_file = ""

        if dataIO.is_valid_json("dlc.json") is False:
            self.owns = False
            show_message("Error", "'dlc.json' not found, functionality has been limited")
        else:
            self.owns = {}
            self.dlc = dataIO.load_json("dlc.json")

        self.basic_edits = {
            self.ui.money_edit: [self.ui.money_dont_change, "money_account:"],
            self.ui.xp_edit: [self.ui.xp_dont_change, "experience_points:"],
            self.ui.loan_limit_edit: [self.ui.loan_limit_dont_change, "loan_limit:"],
        }
        self.skill_edits = {
            self.ui.long_distance_edit: [self.ui.long_distance_dont_change, "long_dist:"],
            self.ui.high_value_cargo_edit: [self.ui.high_value_cargo_dont_change, "heavy:"],
            self.ui.fragile_cargo_edit: [self.ui.fragile_cargo_dont_change, "fragile:"],
            self.ui.urgent_delivery_edit: [self.ui.urgent_delivery_dont_change, "urgent:"],
            self.ui.ecodriving_edit: [self.ui.ecodriving_dont_change, "mechanical:"],
        }

        from PyQt5.QtCore import QRegExp
        from PyQt5.QtGui import QRegExpValidator

        validator_inf = QRegExpValidator(QRegExp("[0-9]{1,9}"))
        for key in self.basic_edits.keys():
            key.setValidator(validator_inf)
            key.textEdited.connect(self.text_edited)

        self.ui.adr_edit.textEdited.connect(self.text_edited)  # TODO: Validator for ADR
        validator_skill = QRegExpValidator(QRegExp("[0-6]{1,1}"))
        for key in self.skill_edits.keys():
            key.setValidator(validator_skill)
            key.textEdited.connect(self.text_edited)

        self.ui.path_button.clicked.connect(self.open_save)
        self.ui.apply.clicked.connect(self.apply_changes)
        self.ui.backup.clicked.connect(self.recover_backup)
        self.ui.second_window.clicked.connect(self.open_second_win)

    def text_edited(self):
        sender = self.sender()
        if sender in self.basic_edits:
            self.basic_edits[sender][0].setChecked(False)
        if sender == self.ui.adr_edit:
            self.ui.adr_dont_change.setChecked(False)
        if sender in self.skill_edits:
            self.skill_edits[sender][0].setChecked(False)

    @staticmethod
    def get_adr(value):
        bin_code = bin(int(value))[2:]
        bin_code = "0" * (6 - len(bin_code)) + bin_code
        r = []
        for i in bin_code:
            r.append(i)
        return r

    def get_adr_from_line(self):
        adr_list = list(self.ui.adr_edit.text())
        for i in adr_list:
            if (i == " ") or (i == ",") or (i == "."):
                adr_list.remove(i)
        return adr_list

    def reopen_file(self):
        self.file_path = ""
        self.old_file = ""
        set_lines("")

        if self.owns is not False:
            self.owns = {}

        for key, value in self.basic_edits.items():
            key.setText("")
            value[0].setChecked(True)

        self.ui.adr_edit.setText("")
        self.ui.adr_dont_change.setChecked(True)
        for key, value in self.skill_edits.items():
            key.setText("")
            value[0].setChecked(True)

        self.ui.apply.setEnabled(False)
        self.ui.backup.setEnabled(False)
        self.ui.second_window.setEnabled(False)
        # return

    def check_save_file(self, file):
        try:
            with open(file, "r") as f:
                self.old_file = f.read()
        except UnicodeDecodeError:
            try:
                from os import system
                system("SII_Decrypt.exe --on_file -i \"{}\"".format(file))
                with open(file, "r") as f:
                    self.old_file = f.read()
                show_message("Success", "File successfully decrypted.")
            except UnicodeDecodeError:
                show_message("Error", "Error to decrypt and open file. Try again.")
                return
        set_lines(self.old_file.split("\n"))

        if self.owns is not False:
            self.owns["base"] = True
            for i in get_array_items(search_line("companies:")):
                for key, value in self.dlc.items():
                    if value in i:
                        self.owns[key] = True

        for key, value in self.basic_edits.items():
            key.setText(str(get_value(search_line(value[1]))))

        adr = self.get_adr(get_value(search_line("adr:")))
        adr_list = ""
        for i in range(6):
            adr_list += adr[i] + "," if i != 5 else adr[i]
        self.ui.adr_edit.setText(adr_list)

        for key, value in self.skill_edits.items():
            key.setText(str(get_value(search_line(value[1]))))

        self.ui.apply.setEnabled(True)
        self.ui.backup.setEnabled(True)
        self.ui.second_window.setEnabled(True)

    def open_save(self):
        from PyQt5.QtWidgets import QFileDialog
        file, _ = QFileDialog.getOpenFileName(parent=self,
                                              caption=self.tr("Choose your save file..."),
                                              filter=self.tr("game.sii"))
        self.reopen_file()
        if file != "":
            self.file_path = file
            self.check_save_file(self.file_path)
        else:
            return

    def apply_changes(self):
        if not self.ui.dont_change_all_inf.isChecked():
            for key, value in self.basic_edits.items():
                if not value[0].isChecked():
                    set_value(search_line(value[1]), key.text())
                value[1].setChecked(False)
            if not self.ui.adr_dont_change.isChecked():
                adr_set = self.get_adr_from_line()
                if len(adr_set) < 6:
                    show_message("Error", "ADR can't have less than 6 elements.")
                elif len(adr_set) > 6:
                    show_message("Error", "ADR can't have more than 6 elements.")
                else:
                    adr_new = int("".join(adr_set), 2)
                    set_value(search_line("adr:"), str(adr_new))
            for key, value in self.skill_edits.items():
                if not value[0].isChecked():
                    set_value(search_line(value[1]), key.text())
                value[1].setChecked(False)
        backup = self.file_path + ".swbak"
        with open(backup, "w") as f:
            f.write(self.old_file)
        with open(self.file_path, "w") as f:
            f.write("\n".join(get_lines()))
        show_message("Success", "Changes successfully applied!")
        self.check_save_file(self.file_path)
        return

    def recover_backup(self):
        try:
            backup = self.file_path + ".swbak"
            f = open(backup, "r")
            with open(self.file_path, "w") as g:
                g.write(f.read())
            f.close()
            from os import remove
            remove(backup)
            show_message("Success", "Backup successfully recovered.")
            self.check_save_file(self.file_path)
        except IOError:
            show_message("Error", "Backup not found.")
            return

    def open_second_win(self):
        from second.script import SecondWindow
        second_win = SecondWindow(self.owns, self)
        second_win.show()
