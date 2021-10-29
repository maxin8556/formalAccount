#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../")
import os
import json
from Utils.utils import get_absolute_path
import datetime
from Utils.JsonTool import JsonTool


#  注入cookie
def addCookie(path, driver):
    with open(path, 'r') as fr:
        cookielist = json.load(fr)
    for cookie in cookielist["cookies"]:
        driver.add_cookie(cookie)


def getCookie(webSource, cookies, userName, passWord):
    cooke_file_path = ""
    if os.name == "nt":
        cooke_file_path = r'D:\MaXin-Study\2021-10-3\FinalVersionAccountForum\cookieData\cookie{}'.format(webSource)
    else:
        cooke_file_path = r'/root/mx/AccountForum/cookieData/cookie{}'.format(webSource)
    save_path = get_absolute_path(cooke_file_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 生成cookie文件
    record = {
        "cookies": cookies,
        "enable": True,
        "name": userName,
        "password": passWord,
        "update_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    file_name = "cookies-" + userName + ".json"
    cookiePath = ""
    if os.name == "nt":
        cookiePath = cooke_file_path + "\\" + file_name
    else:
        cookiePath = cooke_file_path + "/" + file_name

    JsonTool.write_json_file(record, cookiePath, save_path)
