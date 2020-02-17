#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox
from re import search, match, sub


def show_message(title: str, text: str):
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(text)
    box.exec_()


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


def searchlineinunit(lines, term, unit):
    line = searchline(lines, " : " + unit + " {")
    return searchline(lines, term, start=line, cancel="}")


def searchalllines(lines, term):
    matches = []
    start = 0
    while searchline(lines, term, start=start + 1):
        start = searchline(lines, term, start=start + 1)
        matches.append(start)
    if matches is None:
        return None
    return matches


def getvalue(lines, line):
    return search(r": (.+)$", lines[line]).group(1)


def setvalue(lines, line, value):
    name = match(r"(.+):", lines[line]).group(1)
    lines[line] = name + ": " + value


def getunitname(lines, line):
    return search(r" : (.+) {$", lines[line]).group(1)


def getarraylength(lines, line):
    return int(search(r": ([0-9]+)$", lines[line]).group(1))


def getarrayvaluebyindex(lines, line, index):
    return search(r": (.+)$", lines[line + index + 1]).group(1)


def getarrayindexbyvalue(lines, line, value):
    count = 0
    for i in range(getarraylength(lines, line)):
        if getvalue(lines, line + count + 1) == value:
            return count
        count += 1
    return None


def getarrayitems(lines, line):
    items = []
    count = getarraylength(lines, line)
    for i in range(count):
        items.append(search(r": (.+)$", lines[line + i + 1]).group(1))
    if items is None:
        return None
    return items


def addarrayvalue(lines, line, value):
    count = getarraylength(lines, line)
    name = match(r"(.+):", lines[line]).group(1)
    lines[line] = name + ": " + str(count + 1)
    lines.insert(line + count + 1, name + "[" + str(count) + "]: " + value)


def removearrayvalue(lines, line, value):
    name = match(r"(.+):", lines[line]).group(1)
    del lines[line + 1 + getarrayindexbyvalue(lines, line, value)]
    lines[line] = name + ": " + str(getarraylength(lines, line) - 1)
    for i in range(getarraylength(lines, line)):
        lines[line + i + 1] = sub(r"\[[0-9]+\]", "[" + str(i) + "]", lines[line + i + 1])


def changearrayvalue(lines, line, index, value):
    line += index + 1
    setvalue(lines, line, value)
