#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import get
from ast import literal_eval
import os
from statics import github_link, update_config_name
from dataIO import dataIO
from util import util


def get_response_result(url):
    response = get(url)
    return response.status_code == 200, response


def check_path(path):
    current_path = os.getcwd()
    for item in path.split("/"):
        current_path = os.path.join(current_path, item)
        if not os.path.exists(current_path):
            if item.find(".json") > 0:
                open(current_path, "w").close()
            else:
                os.mkdir(current_path)


def check_remote_hashes():
    response_status, response = get_response_result(github_link + "configs/version.cfg")
    if response_status:
        remote_cfg = literal_eval(response.text)
        need_update = []
        for key, value in remote_cfg.items():
            path = key.split("_")
            path = "configs/{}/{}.json".format(path[0], path[1])
            if util.generate_md5(path) != value:
                need_update.append(path)
        return need_update
    return False


def update_configs(is_save, cfg_list):
    if is_save in (0, 1):
        for cfg in cfg_list:
            check_path(cfg)
            response_status, response = get_response_result(github_link + cfg)
            if response_status:
                remote_cfg = literal_eval(response.text)
                if dataIO.is_valid_json(cfg) or os.path.exists(cfg):
                    dataIO.save_json(cfg, remote_cfg)
    if is_save in (1, 3):
        text = str({"answer_updates": is_save == 3,
                    "update_on_start": is_save == 1})
        with open(update_config_name, "w") as f:
            f.write(text)
