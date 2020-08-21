#!/usr/bin/python3
# -*- coding: utf-8 -*-

from json import decoder, load, dump


class DataIO:
    @staticmethod
    def _read_json(filename):
        with open(filename, encoding="utf-8") as f:
            data = load(f)
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
        with open(filename, encoding="utf-8", mode="w") as f:
            dump(data, f, indent=4, separators=(",", " : "))
        try:
            self._read_json(filename)
        except decoder.JSONDecodeError:
            return False
        return True


dataIO = DataIO()
