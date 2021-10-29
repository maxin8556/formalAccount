#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 7/7/21 2:03 PM
# @Author: kevin
# @File: ForumSpider1.py
# @Software: PyCharm

import sys
sys.path.append("../")
import os
import json

import time
import random
import logging

from Utils.CookieOperation import getCookie
from core.SimulationProcess.specificProcess import ForumYorkbbs
from core.elementLocation import YorkbbsElement
from core.setting import FileType
from core.FBInfoDef import FBRetCode
from core.SpiderRetCode import SelenRetCode, BrowserState, AccountLoginStatus, RetCode
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton

LoggerSingleton().init_dict_config(LOGGING_CONFIG)


class YorkbbsSpiderTest(object):

    def __init__(self):
        self._logger = logging.getLogger()

        self.home_url = "http://forum.yorkbbs.ca"
        # 登录Url
        self.loginUrl = "http://forum.yorkbbs.ca/login.aspx"
        # 发帖的URL
        self.post_url = "http://forum.yorkbbs.ca/posttopic.aspx?forumid=12"
        # self.userName = "kevin132"
        # self.passWord = "xx941214"
        self.webSource = "yorkbbs"

        self.userName = "Sameulww"
        self.passWord = "1qaz2wsx"

        self._browser = ForumYorkbbs()  # 浏览器
        self.account_info = {}

    def __del__(self):
        pass

    def spider_basic_state(self, path, login_url):
        """
        检测当前账号登陆状态
        :return: 可用，True；不可用，False
        """
        try:
            # 检测浏览器当前页面状态
            is_on_element = YorkbbsElement.is_on_element

            state_account, cookies = self._browser.check_browser_status(path, self.account_info, self.home_url,
                                                                        is_on_element)
            if state_account == BrowserState.TYPE_ONLINE:  # 在线
                return True, cookies
            elif state_account == BrowserState.TYPE_OFFLINE:  # 离线状态
                # 离线状态，登陆账号
                # 离线状态，登陆账号
                username_element = YorkbbsElement.username_element
                password_element = YorkbbsElement.password_element
                login_element = YorkbbsElement.login_element
                ret, cookies = self._browser.login(self.account_info, login_url, username_element, password_element,
                                                   login_element,self.webSource)

                # 获取cookie并保存文件
                getCookie(self.webSource, cookies, self.userName, self.passWord)

                if SelenRetCode.BROWSER_ERROR == ret:  # 浏览器异常
                    return False, ''
                elif SelenRetCode.FORMAT_ERROR == ret:  # 账号格式错误
                    logging.error("账号格式错误")
                    self.account_info.clear()
                    return False, ''
                else:
                    print("进入论坛发帖版本")
                    # 检测账号登陆状态
                    state = self._browser.check_account_status(self.account_info, is_on_element,self.webSource)
                    if state == AccountLoginStatus.NORMAL:  # 正常
                        # 新增cookie
                        if cookies:
                            logging.info("进入登录状态,cookies已经获取")
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

    def spider_post_list(self, post_url, title, pic_urls, content):

        try:
            print(post_url, title, pic_urls, content)
            time.sleep(random.randint(2, 3))
            logging.info(u"开始论坛发帖，主页URL：{}".format(post_url))

            status = self._browser.open_link(post_url, title, pic_urls, content)
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

    def gen_basic_env(self, account, password, post_url):
        """
        启动浏览器，登陆僵尸账号
        :return: 成功，返回True；失败，返回False
        """
        # 检测账号状态是否正常
        logging.info(u"查网络环境……")
        # 第二个是本地开发测试的
        self.account_info = {"account": account, "password": password, "post_url": post_url}
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
        # """
        # 论坛发帖启动入口
        # :return:
        # """
        title = "增广贤文.警世贤文"
        # pic_urls = ["/root/mx/AccountForum/picture/a.jpg"]
        pic_urls = [r"D:\MaXin-Study\2021-10-3\FinalVersionAccountForum/picture/a.jpg",
                    r"D:\MaXin-Study\2021-10-3\FinalVersionAccountForum/picture/b.jpg"]
        video_urls = ""
        content = "有田不耕仓禀虚，有书不读子孙愚。宝剑锋从磨砺出，梅花香自苦寒来。少壮不知勤学苦，老来方悔读书迟"

        # 构建论坛发帖网络环境
        if not self.gen_basic_env(self.userName, self.passWord, self.post_url):
            print("gen_basic_env进入if")
            time.sleep(random.randint(5, 8))
            return False

        # 判断是否在线
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.spider_basic_state(path, self.loginUrl)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # =================================
        logging.info(u"开始论坛发帖，Homepage:{}".format(self.post_url))

        state = self.spider_post_list(self.post_url, title, pic_urls, content)

        logging.info("论坛发帖最后状态是state:{}".format(state))
        if RetCode.SUCCESS == state:
            logging.info("论坛发帖成功")
            return 0, "论坛发帖成功"
        elif RetCode.REPEAT_FAILED == state:
            logging.info("论坛重复发帖错误")
            return 13, "论坛重复发帖错误"
        elif RetCode.LINK_INVALID == state:
            return 3, "论坛账号cookie失效或者浏览器没有加载上cookie"
        else:
            logging.info("论坛发帖异常失败")
            return 4, "论坛发帖异常失败"


if __name__ == '__main__':
    spider = YorkbbsSpiderTest()
    # path = "../cookieData/cookieYkbbs/cookie-kevin132.json"
    path = ""
    account_info = ""
    print(spider.run(path, account_info))
