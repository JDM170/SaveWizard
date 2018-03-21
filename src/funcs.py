#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox
from re import search, match, sub


class Functions:
    # TODO: My Functions
    @staticmethod
    def showMsgBox(title: str, text: str):
        box = QMessageBox()
        box.setWindowTitle(title)
        box.setText(text)
        box.exec_()
        return

    # TODO: Default functions
    @staticmethod
    def getADR(value):
        bincode = bin(int(value))[2:]
        bincode = "0" * (6 - len(bincode)) + bincode
        r = []
        for i in bincode:
            r.append(i)
        return r

    @staticmethod
    def searchline(lines, term, start=0, cancel=r"thisstringmustnotexist"):
        if search(term, lines[start]):
            return start
        start += 1
        while start <= len(lines) - 1:
            if search(term, lines[start]):
                return start
            if search(cancel, lines[start]):
                return None
            start += 1
        return None

    def searchlineinunit(self, lines, term, unit):
        line = self.searchline(lines, " : " + unit + " {")
        return self.searchline(lines, term, start=line, cancel="}")

    def searchalllines(self, lines, term):
        matches = []
        start = 0
        while self.searchline(lines, term, start=start + 1):
            start = self.searchline(lines, term, start=start + 1)
            matches.append(start)
        if matches is None:
            return None
        return matches

    @staticmethod
    def getvalue(lines, line):
        return search(r": (.+)$", lines[line]).group(1)

    @staticmethod
    def setvalue(lines, line, value):
        name = match(r"(.+):", lines[line]).group(1)
        lines[line] = name + ": " + value

    @staticmethod
    def getunitname(lines, line):
        return search(r" : (.+) {$", lines[line]).group(1)

    @staticmethod
    def getarraylength(lines, line):
        return int(search(r": ([0-9]+)$", lines[line]).group(1))

    @staticmethod
    def getarrayvaluebyindex(lines, line, index):
        return search(r": (.+)$", lines[line + index + 1]).group(1)

    def getarrayindexbyvalue(self, lines, line, value):
        count = 0
        for i in range(self.getarraylength(lines, line)):
            if self.getvalue(lines, line + count + 1) == value:
                return count
            count += 1
        return None

    def getarrayitems(self, lines, line):
        items = []
        count = self.getarraylength(lines, line)
        for i in range(count):
            items.append(search(r": (.+)$", lines[line + i + 1]).group(1))
        if items is None:
            return None
        return items

    def addarrayvalue(self, lines, line, value):
        count = self.getarraylength(lines, line)
        name = match(r"(.+):", lines[line]).group(1)
        lines[line] = name + ": " + str(count + 1)
        lines.insert(line + count + 1, name + "[" + str(count) + "]: " + value)

    def removearrayvalue(self, lines, line, value):
        name = match(r"(.+):", lines[line]).group(1)
        del lines[line + 1 + self.getarrayindexbyvalue(lines, line, value)]
        lines[line] = name + ": " + str(self.getarraylength(lines, line) - 1)
        for i in range(self.getarraylength(lines, line)):
            lines[line + i + 1] = sub(r"\[[0-9]+\]", "[" + str(i) + "]", lines[line + i + 1])

    def changearrayvalue(self, lines, line, index, value):
        line += index + 1
        self.setvalue(lines, line, value)
