#!/usr/bin/python3
# -*- coding: utf-8 -*-

from re import search, match
# from re import search, match, sub
from PyQt5.QtWidgets import QMessageBox
from hashlib import md5
from statics import hash_chunk_size


class CustomFuncs:
    # Custom functions
    def __init__(self):
        self.lines = []

    def set_lines(self, new_lines):
        self.lines = new_lines

    def get_lines(self, index=None):
        if index is not None:
            return self.lines[index]
        return self.lines

    @staticmethod
    def generate_md5(fn):
        try:
            hash_md5 = md5()
            with open(fn, "rb") as f:
                for chunk in iter(lambda: f.read(hash_chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except FileNotFoundError:
            return False

    # Stock functions
    def search_line(self, term, start=0, cancel=r"this_string_must_not_exist"):
        if search(term, self.lines[start]):
            return start
        start += 1
        while start <= len(self.lines) - 1:
            if search(term, self.lines[start]):
                return start
            if search(cancel, self.lines[start]):
                return None
            start += 1
        return None

    def search_line_in_unit(self, term, unit):
        line = self.search_line(" : " + unit + " {")
        return self.search_line(term, start=line, cancel="}")

    def search_all_lines(self, term):
        matches = []
        line = 0
        while self.search_line(term, start=line + 1):
            line = self.search_line(term, start=line + 1)
            matches.append(line)
        if matches is None:
            return None
        return matches

    def get_value(self, line):
        return search(r": (.+)$", self.lines[line]).group(1)

    def set_value(self, line, value):
        name = match(r"(.+):", self.lines[line]).group(1)
        self.lines[line] = name + ": " + value

    # def get_unit_name(self, line):
    #     return search(r" : (.+) {$", self.lines[line]).group(1)

    def get_array_length(self, line):
        return int(search(r": ([0-9]+)$", self.lines[line]).group(1))

    # def get_array_value_by_index(self, line, index):
    #     return search(r": (.+)$", self.lines[line + index + 1]).group(1)

    # def get_array_index_by_value(self, line, value):
    #     count = 0
    #     for i in range(self.get_array_length(line)):
    #         if self.get_value(line + count + 1) == value:
    #             return count
    #         count += 1
    #     return None

    def get_array_items(self, line):
        items = []
        for i in range(self.get_array_length(line)):
            items.append(search(r": (.+)$", self.lines[line + i + 1]).group(1))
        if items is None:
            return None
        return items

    def add_array_value(self, line, value):
        name = match(r"(.+):", self.lines[line]).group(1)
        count = self.get_array_length(line)
        self.lines[line] = name + ": " + str(count + 1)
        self.lines.insert(line + count + 1, name + "[" + str(count) + "]: " + value)

    # def remove_array_value(self, line, value):
    #     name = match(r"(.+):", self.lines[line]).group(1)
    #     del self.lines[line + 1 + self.get_array_index_by_value(line, value)]
    #     count = self.get_array_length(line)
    #     self.lines[line] = name + ": " + str(count - 1)
    #     for i in range(count):
    #         self.lines[line + i + 1] = sub(r"\[[0-9]+]", "[" + str(i) + "]", lines[line + i + 1])

    # def change_array_value(self, line, index, value):
    #     line += index + 1
    #     self.set_value(line, value)


util = CustomFuncs()
