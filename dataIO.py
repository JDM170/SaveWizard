#!/usr/bin/python3
# -*- coding: utf-8 -*-

from json import decoder, load, dump
from os import replace
from os.path import splitext
from random import randint


class InvalidFileIO(Exception):
    pass


class DataIO:
    @staticmethod
    def _read_json(filename):
        with open(filename, encoding="utf-8") as f:
            data = load(f)
        return data

    @staticmethod
    def _save_json(filename, data):
        with open(filename, encoding="utf-8", mode="w") as f:
            dump(data, f, indent=4, sort_keys=True, separators=(",", " : "))
        return data

    def is_valid_json(self, filename):
        """Verifies if json file exists / is readable"""
        try:
            self._read_json(filename)
            return True
        except FileNotFoundError:
            return False
        except decoder.JSONDecodeError:
            return False

    def load_json(self, filename):
        """Loads json file"""
        return self._read_json(filename)

    def save_json(self, filename, data):
        """Atomically saves json file"""
        rnd = randint(1000, 9999)
        path, ext = splitext(filename)
        tmp_file = "{}-{}.tmp".format(path, rnd)
        self._save_json(tmp_file, data)
        try:
            self._read_json(tmp_file)
        except decoder.JSONDecodeError:
            return False
        replace(tmp_file, filename)
        return True


dataIO = DataIO()
