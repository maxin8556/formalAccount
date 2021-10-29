#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton
from Utils.utils import get_absolute_path
from core.setting import FileType, AppType
from spiderData.BloggerSpider import BloggerSpider
from spiderData.HtcSpider import HtcSpider
from spiderData.KomicaSpider import KomicaSpider
from spiderData.MattersSpider import MattersSpider
from spiderData.PixnetSpider import PixnetSpider
from spiderData.RedditSpider import RedditSpider
from spiderData.ShowweSpider import ShowweSpider
from spiderData.TumblrSpider import TumblrSpider
from spiderData.UlifestyleSpider import UlifestyleSpider
from spiderData.YorkbbsSpider import YorkbbsSpider
from spiderData.NybbsSpider import NybbsSpider
from spiderTest.HtcSpiderTest import HtcSpiderTest

LoggerSingleton().init_dict_config(LOGGING_CONFIG)


# def check_acc(cookie_path, account_acc):
#     cookiePath = cookie_path
#     result = os.path.exists(cookiePath)
#     if result:
#         logging.info("登陆账号已存在：{}".format(account_acc))
#         return True, cookiePath
#     else:
#         return False, ""


# 判断状态码
def judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names, fileBytes):
    status, path = check_acc(cookiePath, account_acc)

    if application and account_acc and title and contents and postUrl and names and fileBytes:
        account_info = {
            "appli": application,
            "name": account_acc,
            "title": title,
            "content": contents,
            "postUrl": postUrl,
            "filenames": names,
            "fileBytes": fileBytes
        }
        logging.info("进行账号社交操作")
        # logging.info("进行账号社交操作：{}".format(account_info))
    else:
        logging.info("传入参数异常为：{},{},{},{},{}".format(application, account_acc, title, contents, postUrl,
                                                     names, len(fileBytes)))
        return 5, "输入异常"
    status, msg = object_Social.run(path, account_info)
    logging.info("状态码和信息为:{},{}".format(status, msg))
    if 0 == status:
        return 0, "操作已成功"
    elif 1 == status:
        return 1, "账号不存在"
    elif 2 == status:
        return 2, "账号封停"
    elif 3 == status:
        return 3, "登录失效"
    elif 5 == status:
        return 5, "输入异常"
    elif 6 == status:
        return 6, "网络异常"
    elif 7 == status:
        return 7, "用户名或密码错误"
    elif 9 == status:
        return 9, "帖子不存在或失效"
    elif 12 == status:
        return 12, "无效链接"
    elif 13 == status:
        return 13, "重复操作"
    else:
        return 4, "账号操作异常"


# 检查cookie存在否
def check_acc(cookie_path, account_acc):
    # 如果有cookie
    if cookie_path:
        # print(account_acc)

        # cookie_files = get_absolute_path("./cookieData/cookieYkbbs")
        cookie_files = get_absolute_path(cookie_path)
        list = os.listdir(cookie_files)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            # cookie文件夹下所有的网站账号cookie信息
            path = os.path.join(cookie_files, list[i])
            # print(path)
            file_name = path.split("/")[-1].split("-")[1]
            # print(file_name)

            if account_acc == file_name.replace('.json', ''):
                logging.info("登陆账号已存在：{}".format(account_acc))

                return True, path

            else:
                logging.info("继续查找有无该账号----------")
                continue

        return False, ""
    # 如果没有cookie
    else:
        return True, ""


def tweet_begin(application, account_acc, title, contents, postUrl, names, fileBytes):
    """
    yorkbbs论坛进行发帖入口
    :param application:
    :param account_acc:
    :param title:
    :param contents:
    :param postUrl:
    :param names:
    :param fileBytes:
    :return:
    """

    # york_path = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-forumSpider/AccountForum_Linux/cookieData/cookieYkbbs"
    # status, path = check_acc(york_path, account_acc)
    # 约克论坛
    if AppType.yorkbbs_user == application:
        cookiePath = FileType.cookieYorkbbsPath
        object_Social = YorkbbsSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names, fileBytes)
        return status,msg

    # tumblr
    elif AppType.tumblr_user == application:
        cookiePath = FileType.cookieTumblrPath
        object_Social = TumblrSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names, fileBytes)
        return status,msg

    # reddit  AppType.***需要修改
    elif AppType.reddit_user == application:
        cookiePath = FileType.cookieRedditPath
        # object_Social 需要修改
        object_Social = RedditSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg

        # bloggert  AppType.***需要修改
    elif AppType.blogger_user == application:
        # cookie文件需要修改
        cookiePath = FileType.cookieBloggerPath
        # object_Social 需要修改
        object_Social = BloggerSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg

        # Matters  AppType.***需要修改
    elif AppType.matters_user == application:
        # cookie文件需要修改
        cookiePath = FileType.cookieMattersPath
        # object_Social 需要修改
        object_Social = MattersSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg

    # Komica  AppType.***需要修改
    elif AppType.komica_user == application:
        # cookie文件需要修改
        cookiePath = FileType.cookieKomicaPath
        # object_Social 需要修改
        object_Social = KomicaSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg

        # Komica  AppType.***需要修改
    elif AppType.pixnet_user == application:
        # cookie文件需要修改
        cookiePath = FileType.cookiePixnetPath
        # object_Social 需要修改
        object_Social = PixnetSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg

    # showwe  AppType.***需要修改
    elif AppType.showwe_user == application:
        # cookie文件需要修改
        cookiePath = FileType.cookieShowwePath
        # object_Social 需要修改
        object_Social = ShowweSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg

    # ulifestyle  AppType.***需要修改   出现验证码--已放弃
    elif AppType.ulifestyle_user == application:
        # cookie文件需要修改
        cookiePath = FileType.cookieUlifestylePath
        # object_Social 需要修改
        object_Social = UlifestyleSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg

    # nybbs  AppType.***需要修改   出现验证码--已放弃
    elif AppType.nybbs_user == application:
        # cookie文件需要修改
        cookiePath = FileType.cookieNybbsPath
        # object_Social 需要修改
        object_Social = NybbsSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg

        # nybbs  AppType.***需要修改   出现验证码--已放弃
    elif AppType.htc_user == application:
        # cookie文件需要修改
        cookiePath = FileType.cookieHtcPath
        # object_Social 需要修改
        object_Social = HtcSpider()
        status, msg = judgeStatus(cookiePath, object_Social, account_acc, application, title, contents, postUrl, names,
                                  fileBytes)
        return status, msg