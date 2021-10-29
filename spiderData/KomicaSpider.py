#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 7/7/21 2:03 PM
# @Author: kevin
# @File: ForumSpider1.py
# @Software: PyCharm

import sys
sys.path.append("../")
from Utils.CookieOperation import getCookie
from core.elementLocation import TumblrElement, BloggerElement
import os
import time
import base64
import random
import logging
from core.SimulationProcess.specificProcess import Komica
from core.setting import FileType
from core.FBInfoDef import FBRetCode
from core.SpiderRetCode import SelenRetCode, BrowserState, AccountLoginStatus, RetCode
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton

LoggerSingleton().init_dict_config(LOGGING_CONFIG)


class KomicaSpider(object):

    def __init__(self):
        self._logger = logging.getLogger()

        self.webSource = "komica"
        self.homeUlr = "https://komica.org"
        # 该网站不需要登录
        self.loginUrl = ""
        # 发帖需要填写用户名和邮箱
        self.userName = "BeataBecky"
        # 不需要密码,为了多用户发表,把邮箱等于密码
        self.email = "nialladams931@gmail.com"
        self.passWord = self.email
        # =========================
        self.byte_file = FileType.byte_file
        if not os.path.exists(self.byte_file):  # 判断文件夹是否存在
            os.makedirs(self.byte_file)  # 新建文件夹
        self._browser = Komica()  # 浏览器
        self.account_info = {}



    def spider_post_list(self, post_url, title, media_urls, content,account,password):
        """
        论坛发帖列表
        :param path:
        :param post_url:
        :param title:
        :param media_urls:
        :param content:
        :return:
        """
        try:
            print(title, content)
            time.sleep(random.randint(2, 3))
            logging.info(u"开始论坛发帖，主页URL：{}".format(post_url))

            status = self._browser.open_link(post_url, title, media_urls, content,account,password)

            # # 发帖之后个人主页的截图
            # self._browser.save_screenshot_as_file(r"/root/mx/NEW_AccountForum/picture/tumblrPostSuccess.png")

            logging.info(u"帖子主页进入成功，主页：{}！".format(post_url))
            if FBRetCode.SUCCESS == status:
                return RetCode.SUCCESS
            elif FBRetCode.REPEAT_FAILD == status:
                return RetCode.REPEAT_FAILED
            elif FBRetCode.LINK_OVERDUE == status:
                return RetCode.LINK_INVALID
            else:
                return RetCode.OTHER_ERROR

        except Exception as msg:
            logging.exception(logging.exception(u"论坛发帖异常，异常信息：{}".format(msg)))
            return RetCode.OTHER_ERROR
        finally:
            self._browser.close()

    def gen_basic_env(self, account, password):
        """
        启动浏览器，登陆僵尸账号
        :param account:
        :param password:
        :return:
        """
        # 检测账号状态是否正常
        logging.info(u"查网络环境……")
        # 第二个是本地开发测试的
        self.account_info = {"account": account, "password": password}
        logging.info(u"存在可用僵尸账号，账号：{}".format(self.account_info.get("account")))
        # 检测浏览器是否启动
        if not self._browser.driver:
            if SelenRetCode.SUCCESS != self._browser.open():
                print("进入open")
                self._browser.close()
                return False
        else:
            print("else")
            logging.info(u"论坛发帖浏览器已启动")
        return True

    def run(self, path, account_info):
        """
        论坛发帖启动入口
        :return:
        """
        logging.info("进入{}任务".format(self.webSource))
        account = account_info['name']
        # password = ""
        password = self.passWord

        post_url = account_info['postUrl']
        title = account_info['title']
        # video_urls = account_info['']
        content = account_info['content']
        filenames = account_info['filenames']
        fileBytes = account_info['fileBytes']
        media_urls = []

        if len(filenames) > 0 and len(filenames) != len(fileBytes):
            self._logger.info("进入有名字缺少或没有数据流里面,推文文件名{}长度{},推文数据长度{}".format(filenames,
                                                                            len(filenames), len(fileBytes)))

            return 5, "输入异常"
        elif len(filenames) > 0 and len(filenames) == len(fileBytes):
            self._logger.info("进入有名字也有数据流里面")
            for filename, fileByte in zip(filenames, fileBytes):
                # 二进制数据生成文件
                passed_media = os.path.realpath(self.byte_file + filename)
                print(passed_media)
                # str类型的base64转换成bytes
                fileByte = base64.b64decode(fileByte)
                with open(passed_media, 'wb') as file:
                    file.write(fileByte)
                media_urls.append(passed_media)

        # 构建论坛发帖网络环境
        if not self.gen_basic_env(account, password):
            print("gen_basic_env进入if")
            time.sleep(random.randint(5, 8))
            return 6, "网络异常"


        logging.info(u"开始论坛发帖，Homepage:{}".format(post_url))


        state = self.spider_post_list(post_url, title, media_urls, content,account,password)

        logging.info("论坛发帖最后状态是state:{}".format(state))
        if RetCode.SUCCESS == state:
            logging.info("论坛发帖成功")
            return 0, "论坛发帖成功"
        elif RetCode.REPEAT_FAILED == state:
            logging.info("论坛发帖成功")
            return 13, "论坛重复发帖错误"
        elif RetCode.LINK_INVALID == state:
            return 3, "论坛账号cookie失效或者浏览器没有加载上cookie"
        else:
            logging.info("论坛发帖成功")
            return 4, "论坛发帖异常失败"



