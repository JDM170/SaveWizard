#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from funcs import *
from main_form import *
from wsgiref.validate import validator


class MainWindow(QMainWindow, Ui_MainWindow):
    # TODO: Constructor
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.funcs = Functions()
        #
        self.file_path = ""
        self.oldfile = ""
        self.lines = ""
        self.ownsSC = False
        self.ownsFR = False
        self.ownsIT = False
        self.ownsATS = False
        #
        self.ui.path_button.clicked.connect(self.openSave)
        self.ui.apply.clicked.connect(self.applyChanges)
        self.ui.backup.clicked.connect(self.recoverBackup)
        self.ui.second_window.clicked.connect(self.openSecondWin)
        #
        from PyQt5.QtCore import QRegExp
        from PyQt5.QtGui import QRegExpValidator
        rx_inf = QRegExp("[0-9]{1,9}")
        validator_inf = QRegExpValidator(rx_inf)
        self.ui.money_lineedit.setValidator(validator_inf)
        self.ui.xp_lineedit.setValidator(validator_inf)
        self.ui.loan_limit_lineedit.setValidator(validator_inf)
        #
        rx_skill = QRegExp("[0-6]{1,1}")
        validator_skill = QRegExpValidator(rx_skill)
        self.ui.long_distance_lineedit.setValidator(validator_skill)
        self.ui.high_value_cargo_lineedit.setValidator(validator_skill)
        self.ui.fragile_cargo_lineedit.setValidator(validator_skill)
        self.ui.urgent_delivery_lineedit.setValidator(validator_skill)
        self.ui.ecodriving_lineedit.setValidator(validator_skill)

    # TODO: Custom functions
    def openSecondWin(self):
        from second_script import SecondWindow
        sec_win = SecondWindow(self.ownsSC, self.ownsFR, self.ownsIT, self.ownsATS, self.lines, self)
        sec_win.show()

    def getADRfromLineedit(self):
        adr_list = list(self.ui.adr_lineedit.text())
        i = 0
        for x in adr_list:
            if (adr_list[i] == ",") or (adr_list[i] == ".") or (adr_list[i] == " "):
                del adr_list[i]
                i += 1
            else:
                i += 1
        return adr_list

    def returnLines(self, lines):
        self.lines = lines
        return

    # TODO: Program functions
    def openSave(self):
        from PyQt5.QtWidgets import QFileDialog
        file, _ = QFileDialog.getOpenFileName(parent=self,
                                              caption=self.tr("Choose your file..."),
                                              filter=self.tr("game.sii"),  # ;;Save file (*.sii)
                                              initialFilter=self.tr("game.sii"))
        self.reopen_file()
        if file == "":
            return
        self.file_path = file
        self.checkSaveFile(self.file_path)

    def checkSaveFile(self, file):
        try:
            with open(file, "r") as f:
                self.oldfile = f.read()
        except UnicodeDecodeError:
            try:
                from os import system
                system("SII_Decrypt.exe --on_file -i \"{}\"".format(file))
                with open(file, "r") as f:
                    self.oldfile = f.read()
                self.funcs.showMsgBox("Success", "File successfully decrypted.")
            except UnicodeDecodeError:
                self.funcs.showMsgBox("Error", "Error to decrypt and open file. Try again.")
                return
        self.lines = self.oldfile.split("\n")
        for i in self.lines:
            if "company.volatile.sag_tre.oslo" in i:
                self.ownsSC = True
                self.ui.owns_sc.setChecked(True)
            if "company.volatile.lisette_log.roscoff" in i:
                self.ownsFR = True
                self.ui.owns_fr.setChecked(True)
            if "company.volatile.marina_it.ancona" in i:
                self.ownsIT = True
                self.ui.owns_it.setChecked(True)
            if "company.volatile.gal_oil_gst.oakland" in i:
                self.ownsATS = True
        self.checkAcc()
        self.ui.apply.setEnabled(True)
        self.ui.backup.setEnabled(True)
        self.ui.second_window.setEnabled(True)

    def checkAcc(self):
        self.ui.money_lineedit.setText(str(self.funcs.getvalue(self.lines,
                                                               self.funcs.searchline(self.lines, "money_account:"))))
        self.ui.xp_lineedit.setText(str(self.funcs.getvalue(self.lines,
                                                            self.funcs.searchline(self.lines, "experience_points:"))))
        self.ui.loan_limit_lineedit.setText(str(self.funcs.getvalue(self.lines,
                                                                    self.funcs.searchline(self.lines, "loan_limit:"))))
        #
        adr = self.funcs.getADR(self.funcs.getvalue(self.lines, self.funcs.searchline(self.lines, "adr:")))
        adr_list = ""
        for i in range(6):
            if i != 5:
                elem = adr[i] + ","
            else:
                elem = adr[i]
            adr_list += elem
        self.ui.adr_lineedit.setText(adr_list)
        #
        self.ui.long_distance_lineedit.setText(str(self.funcs.getvalue(self.lines,
                                                                       self.funcs.searchline(self.lines, "long_dist:"))))
        self.ui.high_value_cargo_lineedit.setText(str(self.funcs.getvalue(self.lines,
                                                                          self.funcs.searchline(self.lines, "heavy:"))))
        self.ui.fragile_cargo_lineedit.setText(str(self.funcs.getvalue(self.lines,
                                                                       self.funcs.searchline(self.lines, "fragile:"))))
        self.ui.urgent_delivery_lineedit.setText(str(self.funcs.getvalue(self.lines,
                                                                         self.funcs.searchline(self.lines, "urgent:"))))
        self.ui.ecodriving_lineedit.setText(str(self.funcs.getvalue(self.lines,
                                                                    self.funcs.searchline(self.lines, "mechanical:"))))

    def applyChanges(self):
        self.applyChanges_1()
        self.applyChanges_2()
        backup = self.file_path + ".swbak"
        with open(backup, "w") as f:
            f.write(self.oldfile)
        with open(self.file_path, "w") as f:
            f.write("\n".join(self.lines))
        self.funcs.showMsgBox("Success", "Changes successfully applied!")
        self.checkSaveFile(self.file_path)
        return

    def applyChanges_1(self):
        if not self.ui.money_dont_change.isChecked():
            self.funcs.setvalue(self.lines,
                                self.funcs.searchline(self.lines, "money_account:"),
                                str(self.ui.money_lineedit.text()))
        #
        if not self.ui.xp_dont_change.isChecked():
            self.funcs.setvalue(self.lines,
                                self.funcs.searchline(self.lines, "experience_points:"),
                                str(self.ui.xp_lineedit.text()))
        #
        if not self.ui.loan_limit_dont_change.isChecked():
            self.funcs.setvalue(self.lines,
                                self.funcs.searchline(self.lines, "loan_limit:"),
                                str(self.ui.loan_limit_lineedit.text()))
        #
        self.ui.money_dont_change.setChecked(False)
        self.ui.xp_dont_change.setChecked(False)
        self.ui.loan_limit_dont_change.setChecked(False)

    def applyChanges_2(self):
        if not self.ui.adr_dont_change.isChecked():
            adrset = self.getADRfromLineedit()
            if len(adrset) > 6:
                self.funcs.showMsgBox("Error", "ADR can't have more than 6 elements.")
            else:
                adrnew = int("".join(adrset), 2)
                self.funcs.setvalue(self.lines,
                                    self.funcs.searchline(self.lines, "adr:"),
                                    str(adrnew))
        #
        if not self.ui.long_distance_dont_change.isChecked():
            self.funcs.setvalue(self.lines,
                                self.funcs.searchline(self.lines, "long_dist:"),
                                str(self.ui.long_distance_lineedit.text()))
        #
        if not self.ui.high_value_cargo_dont_change.isChecked():
            self.funcs.setvalue(self.lines,
                                self.funcs.searchline(self.lines, "heavy:"),
                                str(self.ui.high_value_cargo_lineedit.text()))
        #
        if not self.ui.fragile_cargo_dont_change.isChecked():
            self.funcs.setvalue(self.lines,
                                self.funcs.searchline(self.lines, "fragile:"),
                                str(self.ui.fragile_cargo_lineedit.text()))
        #
        if not self.ui.urgent_delivery_dont_change.isChecked():
            self.funcs.setvalue(self.lines,
                                self.funcs.searchline(self.lines, "urgent:"),
                                str(self.ui.urgent_delivery_lineedit.text()))
        #
        if not self.ui.ecodriving_dont_change.isChecked():
            self.funcs.setvalue(self.lines,
                                self.funcs.searchline(self.lines, "mechanical:"),
                                str(self.ui.ecodriving_lineedit.text()))
        #
        self.ui.adr_dont_change.setChecked(False)
        self.ui.long_distance_dont_change.setChecked(False)
        self.ui.high_value_cargo_dont_change.setChecked(False)
        self.ui.fragile_cargo_dont_change.setChecked(False)
        self.ui.urgent_delivery_dont_change.setChecked(False)
        self.ui.ecodriving_dont_change.setChecked(False)

    def recoverBackup(self):
        backup = self.file_path + ".swbak"
        try:
            f = open(backup, "r")
            with open(self.file_path, "w") as g:
                g.write(f.read())
            f.close()
            from os import remove
            remove(backup)
            self.funcs.showMsgBox("Success", "Backup successfully recovered.")
            self.checkSaveFile(self.file_path)
            return
        except:
            self.funcs.showMsgBox("Error", "Backup not found.")
            return

    def reopen_file(self):
        self.file_path = ""
        self.oldfile = ""
        self.lines = ""
        #
        self.ownsSC = False
        self.ownsFR = False
        self.ownsIT = False
        self.ui.owns_sc.setChecked(False)
        self.ui.owns_fr.setChecked(False)
        self.ui.owns_it.setChecked(False)
        self.ownsATS = False
        #
        self.ui.money_lineedit.setText("")
        self.ui.money_dont_change.setChecked(False)
        self.ui.xp_lineedit.setText("")
        self.ui.xp_dont_change.setChecked(False)
        self.ui.loan_limit_lineedit.setText("")
        self.ui.loan_limit_dont_change.setChecked(False)
        #
        self.ui.adr_lineedit.setText("")
        self.ui.adr_dont_change.setChecked(False)
        self.ui.long_distance_lineedit.setText("")
        self.ui.long_distance_dont_change.setChecked(False)
        self.ui.high_value_cargo_lineedit.setText("")
        self.ui.high_value_cargo_dont_change.setChecked(False)
        self.ui.fragile_cargo_lineedit.setText("")
        self.ui.fragile_cargo_dont_change.setChecked(False)
        self.ui.urgent_delivery_lineedit.setText("")
        self.ui.urgent_delivery_dont_change.setChecked(False)
        self.ui.ecodriving_lineedit.setText("")
        self.ui.ecodriving_dont_change.setChecked(False)
        #
        self.ui.apply.setEnabled(False)
        self.ui.backup.setEnabled(False)
        self.ui.second_window.setEnabled(False)
        return


if __name__ == '__main__':
    from sys import argv, exit
    from PyQt5.QtWidgets import QApplication
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
