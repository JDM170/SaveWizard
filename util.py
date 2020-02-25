#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox
from re import search, match, sub
lines = ''


def set_lines(from_other):
    global lines
    lines = from_other


def get_lines():
    global lines
    return lines


def show_message(title, text):
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(text)
    box.exec_()


def search_line(term, start=0, cancel=r"this_string_must_not_exist"):
    global lines
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


def search_line_in_unit(term, unit):
    global lines
    line = search_line(" : " + unit + " {")
    return search_line(term, start=line, cancel="}")


def search_all_lines(term):
    global lines
    matches = []
    start = 0
    while search_line(term, start=start + 1):
        start = search_line(term, start=start + 1)
        matches.append(start)
    if matches is None:
        return None
    return matches


def get_value(line):
    global lines
    return search(r": (.+)$", lines[line]).group(1)


def set_value(line, value):
    global lines
    name = match(r"(.+):", lines[line]).group(1)
    lines[line] = name + ": " + value


def get_unit_name(line):
    global lines
    return search(r" : (.+) {$", lines[line]).group(1)


def get_array_length(line):
    global lines
    return int(search(r": ([0-9]+)$", lines[line]).group(1))


def get_array_value_by_index(line, index):
    global lines
    return search(r": (.+)$", lines[line + index + 1]).group(1)


def get_array_index_by_value(line, value):
    global lines
    count = 0
    for i in range(get_array_length(line)):
        if get_value(line + count + 1) == value:
            return count
        count += 1
    return None


def get_array_items(line):
    global lines
    items = []
    for i in range(get_array_length(line)):
        items.append(search(r": (.+)$", lines[line + i + 1]).group(1))
    if items is None:
        return None
    return items


def add_array_value(line, value):
    global lines
    name = match(r"(.+):", lines[line]).group(1)
    count = get_array_length(line)
    lines[line] = name + ": " + str(count + 1)
    lines.insert(line + count + 1, name + "[" + str(count) + "]: " + value)


def remove_array_value(line, value):
    global lines
    name = match(r"(.+):", lines[line]).group(1)
    del lines[line + 1 + get_array_index_by_value(line, value)]
    count = get_array_length(line)
    lines[line] = name + ": " + str(count - 1)
    for i in range(count):
        lines[line + i + 1] = sub(r"\[[0-9]+\]", "[" + str(i) + "]", lines[line + i + 1])


def change_array_value(line, index, value):
    global lines
    line += index + 1
    set_value(line, value)
