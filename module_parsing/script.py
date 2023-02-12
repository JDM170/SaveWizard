#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import get
from ast import literal_eval
import os
from statics import github_link, update_config_name
from dataIO import dataIO
from util import util


def get_response_result(url):
    """
    Getting the result from a given url
    :param url: url where we get data
    :return: status code (True or False), response body
    """
    response = get(url)
    return response.status_code == 200, response


def check_path(path):
    """
    Checks if the path exists (if not, creates it)
    :param path: path to check
    """
    current_path = os.getcwd()
    for item in path.split("/"):
        current_path = os.path.join(current_path, item)
        if not os.path.exists(current_path):
            if item.find(".json") > 0:
                open(current_path, "w").close()
            else:
                os.mkdir(current_path)


def check_remote_hashes():
    # response_status, response = get_response_result(github_link + "configs/version.cfg")
    response_status, response = get_response_result(github_link + "configs/version_new.cfg")
    if response_status:
        remote_cfg = literal_eval(response.text)
        need_update = []
        for game, cfg in remote_cfg.items():
            for f_name, f_hash in cfg.items():
                path = "configs/{}/{}.json".format(game, f_name)
                if util.generate_md5(path) != f_hash:
                    need_update.append(path)
        return need_update
    return False


def update_configs(cfg_list, ans_upd=0):
    """
    :param cfg_list: config list to update
    :param ans_upd: ask user to update configs, update or not, remember answer or not
    """
    if ans_upd in (0, 1):
        for cfg in cfg_list:
            check_path(cfg)
            response_status, response = get_response_result(github_link + cfg)
            if response_status:
                remote_cfg = literal_eval(response.text)
                if dataIO.is_valid_json(cfg) or os.path.exists(cfg):
                    dataIO.save_json(cfg, remote_cfg)
    if ans_upd in (1, 3):
        with open(update_config_name, "w") as f:
            f.write(str({"answer_updates": ans_upd == 3, "update_on_start": ans_upd == 1}))
