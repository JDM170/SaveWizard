#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import system, remove
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QFileDialog
from .form import Ui_MainWindow
from util import *
from dataIO import dataIO
from module_second.script import SecondWindow


class MainWindow(QDialog, Ui_MainWindow):
    def __init__(self, selected_game, parent=None):
        # Setup UI
        QDialog.__init__(self, parent, flags=Qt.Window)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_path = ""
        self.old_file = ""

        self.selected_game = selected_game
        self.owns = {}
        self.dlc = {}

        # Editing label to show what configs chosen
        self.chosen_cfg_text = self.ui.chosen_cfgs.text()
        self.ui.chosen_cfgs.setText("{} {}".format(self.chosen_cfg_text, selected_game.upper()))

        # Storing edits with his checkboxes and file-lines
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

        # Setting up validators for edits
        basic_validator = QRegExpValidator(QRegExp("[0-9]{,9}"))
        for key in self.basic_edits.keys():
            key.setValidator(basic_validator)
            key.textEdited.connect(self.text_edited)

        adr_validator_text = ""
        for i in range(6):
            adr_validator_text += r"\d[., ]?" if i != 5 else r"\d"
        self.ui.adr_edit.textEdited.connect(self.text_edited)
        self.ui.adr_edit.setValidator(QRegExpValidator(QRegExp(adr_validator_text)))
        skills_validator = QRegExpValidator(QRegExp("[0-6]{,1}"))
        for key in self.skill_edits.keys():
            key.setValidator(skills_validator)
            key.textEdited.connect(self.text_edited)

        # Connecting buttons
        self.ui.path_button.clicked.connect(self.open_file_dialog)
        self.ui.cfg_button.clicked.connect(self.change_configs)
        self.ui.backup.clicked.connect(self.recover_backup)
        self.ui.second_window.clicked.connect(self.open_second_win)
        self.ui.apply.clicked.connect(self.apply_changes)

        self.check_config()
        self.clear_form_data()

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

    def check_config(self):
        cfg_path = "configs/{}/dlc.json".format(self.selected_game)
        if dataIO.is_valid_json(cfg_path) is False:
            self.owns = False
            QMessageBox.warning(self, "Warning", "'dlc.json' from '{}' have errors or not found, "
                                                 "functionality has been limited".format(self.selected_game))
        else:
            self.owns = {}
            self.dlc = dataIO.load_json(cfg_path)

    def clear_form_data(self):
        self.file_path = ""
        self.old_file = ""
        util.set_lines([])

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

    def get_file_data(self, file):
        try:
            with open(file) as f:
                self.old_file = f.read()
        except UnicodeDecodeError:
            try:
                system("SII_Decrypt.exe --on_file -i \"{}\"".format(file))
                with open(file) as f:
                    self.old_file = f.read()
                QMessageBox.information(self, "Success", "File successfully decrypted.")
            except UnicodeDecodeError:
                QMessageBox.critical(self, "Error", "Error to decrypt and open file. "
                                                    "Try again.\nIf you still get error on this step, "
                                                    "try to change \"uset g_save_format\" to 2, resave "
                                                    "game and try again.")
                return
        util.set_lines(self.old_file.split("\n"))

        if self.owns is not False:
            self.owns["base"] = True
            companies = util.get_array_items(util.search_line("companies:"))
            for key, value in self.dlc.items():
                if value in companies:
                    self.owns[key] = True

        for key, value in self.basic_edits.items():
            key.setText(util.get_value(util.search_line(value[1])))

        adr = self.get_adr(util.get_value(util.search_line("adr:")))
        adr_list = ""
        for i in range(6):
            adr_list += adr[i] + "," if i != 5 else adr[i]
        self.ui.adr_edit.setText(adr_list)

        for key, value in self.skill_edits.items():
            key.setText(util.get_value(util.search_line(value[1])))

        self.ui.apply.setEnabled(True)
        self.ui.backup.setEnabled(True)
        self.ui.second_window.setEnabled(True)

    def open_file_dialog(self):
        file_path, file_name = QFileDialog.getOpenFileName(parent=self,
                                                           caption=self.tr("Choose your save file..."),
                                                           filter=self.tr("game.sii"))
        self.clear_form_data()
        if file_path != "":
            self.file_path = file_path
            self.get_file_data(file_path)
        else:
            return

    def change_configs(self):
        box = QMessageBox(QMessageBox.Warning, "Warning", "Do you really want to load other configs?\n"
                                                          "Your current changes won't be saved.")
        box.addButton("Yes", QMessageBox.YesRole)
        box.addButton("No", QMessageBox.NoRole)
        if box.exec() == 0:
            self.clear_form_data()
            self.selected_game = "ets2" if self.selected_game == "ats" else "ats"
            self.ui.chosen_cfgs.setText("{} {}".format(self.chosen_cfg_text, self.selected_game.upper()))
            self.check_config()

    def recover_backup(self):
        try:
            backup_path = self.file_path + ".swbak"
            with open(self.file_path, "w") as current:
                with open(backup_path) as backup:
                    current.write(backup.read())
            remove(backup_path)
            QMessageBox.information(self, "Success", "Backup successfully recovered.")
            self.get_file_data(self.file_path)
        except IOError:
            QMessageBox.critical(self, "Error", "Backup not found.")

    def open_second_win(self):
        second_win = SecondWindow(self.selected_game, self.owns, self)
        second_win.exec()

    def apply_changes(self):
        if not self.ui.dont_change_all_inf.isChecked():
            for key, value in self.basic_edits.items():
                if value[0].isChecked() is False:
                    util.set_value(util.search_line(value[1]), key.text())
                    value[0].setChecked(True)
            if self.ui.adr_dont_change.isChecked() is False:
                adr_set = self.get_adr_from_line()
                if len(adr_set) < 6:
                    QMessageBox.critical(self, "Error", "ADR can't have less than 6 elements.")
                elif len(adr_set) > 6:
                    QMessageBox.critical(self, "Error", "ADR can't have more than 6 elements.")
                else:
                    adr_new = int("".join(adr_set), 2)
                    util.set_value(util.search_line("adr:"), str(adr_new))
            for key, value in self.skill_edits.items():
                if value[0].isChecked() is False:
                    util.set_value(util.search_line(value[1]), key.text())
                    value[0].setChecked(True)
        backup = self.file_path + ".swbak"
        with open(backup, "w") as f:
            f.write(self.old_file)
        with open(self.file_path, "w") as f:
            f.write("\n".join(util.get_lines()))
        QMessageBox.information(self, "Success", "Changes successfully applied!")
        self.get_file_data(self.file_path)
