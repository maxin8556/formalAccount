#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 7/7/21 2:03 PM
# @Author: kevin
# @File: ForumSpider1.py
# @Software: PyCharm

import sys

sys.path.append("../")
import os
import time
import base64
import random
import logging
from core.SimulationProcess.specificProcess import Matters
from core.FBInfoDef import FBRetCode
from core.SpiderRetCode import SelenRetCode, BrowserState, AccountLoginStatus, RetCode
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton
from Utils.CookieOperation import getCookie
from core.elementLocation import RedditElement, MattersElement
from core.setting import FileType

LoggerSingleton().init_dict_config(LOGGING_CONFIG)


class MattersSpider(object):

    def __init__(self):
        self._logger = logging.getLogger()

        # =========================
        # 网站主页,注入cookie时用的
        self.home_url = "https://www.matters.news"
        self.webSource = 'matters'
        # 登录Url
        self.loginUrl = "https://www.matters.news"


        # self.passWord = "bblove123"
        self.passWord = "maxin123"

        # =========================
        self._browser = Matters()  # 浏览器
        self.account_info = {}

        self.byte_file = FileType.byte_file
        if not os.path.exists(self.byte_file):  # 判断文件夹是否存在
            os.makedirs(self.byte_file)  # 新建文件夹

    def __del__(self):
        pass

    def spider_basic_state(self, path, login_url):
        """
        检测当前账号登陆状态
        :return: 可用，True；不可用，False
        """
        try:
            # 检测浏览器当前页面状态
            # 该元素是判断用户是否在线的元素
            is_on_element = MattersElement.is_on_element
            state_account, cookies = self._browser.check_browser_status(path, self.account_info, self.home_url,
                                                                        is_on_element)
            if state_account == BrowserState.TYPE_ONLINE:  # 在线
                return True, cookies
            elif state_account == BrowserState.TYPE_OFFLINE:  # 离线状态
                # 离线状态，登陆账号
                username_element = RedditElement.username_element
                password_element = RedditElement.password_element
                login_element = RedditElement.login_element
                ret, cookies = self._browser.login(self.account_info, login_url, username_element, password_element,
                                                   login_element,self.webSource)

                # 登录之后获取cookie并保存到文件
                getCookie(self.webSource, cookies, self.account_info['account'], self.account_info['password'])

                if SelenRetCode.BROWSER_ERROR == ret:  # 浏览器异常
                    return False, ''
                elif SelenRetCode.FORMAT_ERROR == ret:  # 账号格式错误
                    logging.error("账号格式错误")
                    self.account_info.clear()
                    return False, ''
                else:
                    logging.info(">>>>>>>>>>>>进入论坛发帖版本<<<<<<<<<<<<<")
                    # 检测账号登陆状态
                    state = self._browser.check_account_status(self.account_info,is_on_element,self.webSource)
                    if state == AccountLoginStatus.NORMAL:  # 正常
                        # 新增cookie
                        if cookies:
                            # logging.info("进入和cookies{}".format(cookies))
                            logging.info("进入登录状态,cookie已经获取")
                            return True, cookies
                        else:
                            logging.error("账号没有cookie不可用")
                            self.account_info.clear()
                            return False, ''
                    elif state == AccountLoginStatus.PASSWORD_ERROR:  # 密码错误
                        logging.error("密码错误")
                        self.account_info.clear()
                        return False, ''
                    else:  # 账号不可用
                        self._browser.clear_cookies()
                        logging.error("账号不可用")
                        self.account_info.clear()
                        return False, ''

            elif state_account == BrowserState.TYPE_EXCEPTION:
                return False, ''
            else:  # 账号无效
                self._browser.clear_cookies()
                logging.error("账号无效")
                self.account_info.clear()
                return False, ''
        except Exception as msg:
            logging.exception(u"浏览器账号登陆状态检测异常，异常信息：{}".format(msg))
            return False, ''

    def spider_post_list(self, post_url, title, media_urls, content):
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

            status = self._browser.open_link(post_url, title, media_urls, content)

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

    # def run(self, path, account_info):
    def run(self, path, account_info):
        """
        论坛发帖启动入口
        :return:
        """
        logging.info(">>>>>>>>>>>>>>>进入{}任务<<<<<<<<<<<<".format(self.webSource))
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

        # 判断是否在线
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        logging.info(">>>>>>>>>>>开始判断是否{}在线<<<<<<<<<<<".format(self.webSource))
        self.spider_basic_state(path, self.loginUrl)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        logging.info(u"开始论坛发帖，Homepage:{}".format(post_url))


        state = self.spider_post_list(post_url, title, media_urls, content)

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



