# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('../')
from Utils.CookieOperation import getCookie
import time
import random
import logging
from core.FBInfoDef import FBRetCode
from core.SpiderRetCode import SelenRetCode, BrowserState, AccountLoginStatus, RetCode
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton
from core.elementLocation import TumblrElement
from core.SimulationProcess.specificProcess import Komica

LoggerSingleton().init_dict_config(LOGGING_CONFIG)


class KomicaSpiderTest(object):

    def __init__(self):
        self._logger = logging.getLogger()
        # 登录Url   该网站不需要登录
        self.homeUlr = "https://komica.org"
        self.loginUrl = ""
        # 发帖的URL   生活消费相关

        # https://eclair.nagatoyuki.org/outremer/   海外  需要修改海外

        self.post_url = "http://gzone-anime.info/UnitedSites/shopping/"

        self.webSource = "komica"
        # # 发帖需要填写用户名和邮箱
        # self.userName = "GodDD"
        # # 不需要密码,为了多用户发表,把邮箱等于密码
        # self.email = "maxin@gmail.com"
        # # 发帖需要填写用户名和邮箱
        # self.userName = "GodDD"
        # # 不需要密码,为了多用户发表,把邮箱等于密码
        # self.email = "maxin@gmail.com"
        # 发帖需要填写用户名和邮箱
        self.userName = "BeataBecky"
        # 不需要密码,为了多用户发表,把邮箱等于密码
        self.email = "nialladams931@gmail.com"


        self.passWord = self.email

        self._browser = Komica()  # 浏览器
        self.account_info = {}

    def __del__(self):
        pass

    def spider_post_list(self, post_url, title, pic_urls, content):
        print("spider_post_list 发帖开始")
        try:
            print(title, content)
            time.sleep(random.randint(2, 3))
            logging.info(u"开始论坛发帖，主页URL：{}".format(post_url))
            status = self._browser.open_link(post_url, title, pic_urls, content,self.userName,self.passWord)
            print(status)
            print(type(status))
            # self._browser.save_screenshot_as_file("post.png")
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
        # 社区
        community = "r/maxin8556"
        title = "明·朱熹《增广贤文.警世贤文》之勤奋篇"
        # pic_urls = ["/root/mx/M_AccountForum_Linux/spiderTest/a.jpg",
        #             "/root/mx/M_AccountForum_Linux/spiderTest/b.jpg"]
        pic_urls = [r"D:\MaXin-Study\2021-10-3\FinalVersionAccountForum\picture\a.jpg"]

        video_urls = ""
        content = "有田不耕仓禀虚，有书不读子孙愚"

        # 构建论坛发帖网络环境
        if not self.gen_basic_env(self.userName, self.passWord, self.post_url):
            print("gen_basic_env进入if")
            time.sleep(random.randint(5, 8))
            return False

        # 判断是否在线
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # self.spider_basic_state(path, self.loginUrl)
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
    t1 = time.time()
    spider = KomicaSpiderTest()
    # path = r"D:\MaXin-Study\2021-10-3\FinalVersionAccountForum\cookieData\cookietumblr\cookies-maxin8556@163.com.json"
    path = ""
    account_info = ""
    print(spider.run(path, account_info))
    print('耗时:', time.time() - t1)
