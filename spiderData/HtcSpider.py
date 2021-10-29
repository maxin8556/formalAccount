#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

sys.path.append("../")
import os
import time
import base64
import random
import logging
from core.SimulationProcess.specificProcess import Reddit, Htc
from core.FBInfoDef import FBRetCode
from core.SpiderRetCode import SelenRetCode, BrowserState, AccountLoginStatus, RetCode
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton
from Utils.CookieOperation import getCookie
from core.elementLocation import RedditElement, HtcElement
from core.setting import FileType

LoggerSingleton().init_dict_config(LOGGING_CONFIG)


class HtcSpider(object):

    def __init__(self):
        self._logger = logging.getLogger()

        # =========================
        # 网站主页,注入cookie时用的
        self.home_url = "https://community.htc.com/tw/hero.php"
        self.webSource = 'htc'
        # 登录Url
        self.loginUrl = "https://account.htcvive.com/login/saml?request=eyJJRCI6IjA3NDNiOGI0LTFlNGEtNDdhOC1iN2ZkLWE1NTcwM2I1OGM0NiIsIklzc3VlciI6ImFjY291bnQuaHRjLmNvbSIsInRpbWVzdGFtcCI6IjIwMjEtMTAtMjVUMTI6MTc6NTIuMjk3WiIsIk5vdE9uT3JBZnRlciI6IjIwMjEtMTAtMjVUMTI6MTk6NTIuMjk3WiIsIlNlcnZpY2VQcm92aWRlciI6IjI4ZmNiNmQ5LTliOWItNDg0My1hOTJjLTIwNTQ1Y2UzYTk5OCIsIkF1dGhvcml0aWVzIjoiIiwiRmllbGRzIjoiZm49MSxsbj0xIiwiQ2FsbGJhY2siOiJodHRwczovL2FjY291bnQuaHRjdml2ZS5jb20vUkFNL1NTLy9hcGkvb2F1dGgvdjEvYXV0aG9yaXplIiwiRGVzdGluYXRpb24iOiJodHRwczovL2FjY291bnQuaHRjdml2ZS5jb20vbG9naW4vc2FtbCIsIlZlcnNpb24iOjIsIlJlbGF5U3RhdGUiOiIxdTIxV3pxcndtZm05U29nSjhYTzExWUZaVjF3VkwwYXhBNkcvcUx0SXY1SUZXWkhqS3ZEdlBtanFqQit4Mmt5bURQb1YwTnN1SnM3VW5KVHVXWjVwWkh5c2paMTVoL2Q1ajVhRG5CVXZBRVV5TzhjR09xVmZHZU9QYS82UG05eHZuQjhkVWc1UVk1MnJkYkxjYk92VmROQkhsNFh4VFJwT3orYTdlMmZMQ2Z6dEM1dS9HNEVjMzJvUWcrSnQ3YnVzMHFkR2R4ZUl0TUNmMGFhRUVQdkdybFJ3dGRaUGtNeStLOEZlQzlnYzdRPSIsIkkxOG5JZCI6InR3Y29tbXVuaXR5IiwiVmlld1R5cGUiOiJwb3B1cCJ9&sigalg=SHA1withRSA&state=eyJyZWRpcmVjdGlvblVybCI6Imh0dHBzOi8vY29tbXVuaXR5Lmh0Yy5jb20vdHcvaGVyby5waHAiLCJjbGllbnRJZCI6IjI4ZmNiNmQ5LTliOWItNDg0My1hOTJjLTIwNTQ1Y2UzYTk5OCIsIm5vbmNlIjoiOTMwOTIyNzM5OTc4MTQ4NjY5In0%3D&signature=ZgHNn3bJG5PDJn9%2BE9d%2BnQy4EK1M58pZds8o4fPcocWBDZi0perRqzFQKUwcr2irguPQtGU7HldTEFbZ96oKjMBpQ19mdgkgk2LN4HLDJRYUfJy6j4eX188HsnK3z6Ba/z16RjL%2Bs/l%2BSbtu0FwBxg/X4rr2sTyvXjcdcq%2B1FLyH/Ie7yTszCraPAPIw5ij7ifDTYr1TbTn2O6qIR3H5uLbETPe2u0l%2Bs6xYrQM8Ira2G2X52%2BJoX%2BeJOjmQ1wRcH3TK4CoNVbsnT6hMVh9o4rEKGIIqNq7saXwchVz3DMFPK6odoe1mmEhai7xaccmq2WVfd2VtN6yinpFkMhlHag%3D%3D"
        self.passWord = "Maxin123@"
        # =========================
        self._browser = Htc()  # 浏览器
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
            cookie_is_on_element = HtcElement.cookie_is_on_element
            login_is_on_element = HtcElement.login_is_on_element
            state_account, cookies = self._browser.check_browser_status(path, self.account_info, self.home_url,
                                                                        cookie_is_on_element)
            if state_account == BrowserState.TYPE_ONLINE:  # 在线
                return True, cookies
            elif state_account == BrowserState.TYPE_OFFLINE:  # 离线状态
                # 离线状态，登陆账号
                username_element = HtcElement.username_element
                password_element = HtcElement.password_element
                login_element = HtcElement.login_element
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
                    state = self._browser.check_account_status(self.account_info,login_is_on_element,self.webSource)
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



