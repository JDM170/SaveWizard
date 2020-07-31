#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import get
from hashlib import md5
from ast import literal_eval
import os
from dataIO import dataIO
from util import github_link, update_config_name


def send_response(txt):
    response = get(txt)
    return response if response.status_code == 200 else False


def generate_md5(fn):
    hash_md5 = md5()
    try:
        with open(fn, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        return False


def check_files(path):
    temp = os.getcwd()
    for item in path.split("/"):
        temp = os.path.join(temp, item)
        if not os.path.exists(temp):
            if item.find(".json") > 0:
                f = open(temp, "w")
                f.close()
            else:
                os.mkdir(temp)


def check_remote_hashes():
    response = send_response(github_link + "configs/version.cfg")
    if response is not False:
        remote_cfg = literal_eval(response.text)
        need_to_be_updated = []
        for key, value in remote_cfg.items():
            path = key.split("_")
            path = "configs/{}/{}.json".format(path[0], path[1])
            if generate_md5(path) != value:
                need_to_be_updated.append(path)
        return need_to_be_updated
    return False


def update_configs(is_save, cfg_list):
    if is_save in (0, 1):
        for cfg in cfg_list:
            check_files(cfg)
            response = send_response(github_link + cfg)
            if response is not False:
                remote_cfg = literal_eval(response.text)
                if dataIO.is_valid_json(cfg) or os.path.exists(cfg):
                    dataIO.save_json(cfg, remote_cfg)
    if is_save in (1, 3):
        text = str({"answer_updates": is_save == 3,
                    "update_on_start": is_save == 1})
        with open(update_config_name, "w") as f:
            f.write(text)
