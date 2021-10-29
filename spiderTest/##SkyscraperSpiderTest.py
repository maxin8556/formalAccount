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
from core.elementLocation import SkyscraperElement
from core.SimulationProcess.specificProcess import Skyscrapercity

LoggerSingleton().init_dict_config(LOGGING_CONFIG)


class SkyscraperSpiderTest(object):

    def __init__(self):
        self._logger = logging.getLogger()
        # 网站主页,注入cookie时用的
        self.home_url = "https://www.skyscrapercity.com/"
        # 登录Url 用登录网站需要验证,直接点击登录不需要验证
        # self.loginUrl = "https://www.skyscrapercity.com/login"
        self.loginUrl = "https://www.skyscrapercity.com"
        # 发帖的URL    发帖前需要看有没有上次发布失败的内容
        self.post_url = "https://www.skyscrapercity.com/forums/north-american-skyscrapers-forum.103/post-thread"

        self.webSource = "skyscrapercity"

        # self.userName = "maxin8556@163.com"
        # self.passWord = "maxin123"
        # self.userName = "mx13155131065@163.com"
        # self.passWord = "maxin123"
        # 2843605060@qq.com  用户名GodM,密码 GodM123@
        self.userName = "2843605060@qq.com"
        self.passWord = "GodM123@"

        self._browser = Skyscrapercity()  # 浏览器
        self.account_info = {}

    def __del__(self):
        pass

    # 注入cookie判断登录状态,第一次肯定是登录失败需要输入账号密码
    def spider_basic_state(self, path, login_url):

        try:
            # 判断用户是否在线
            # 该元素是判断用户是否在线的元素
            is_on_element = SkyscraperElement.is_on_element
            state_account, cookies = self._browser.check_browser_status(path, self.account_info, self.home_url,
                                                                        is_on_element)
            if state_account == BrowserState.TYPE_ONLINE:  # 在线
                return True, cookies
            elif state_account == BrowserState.TYPE_OFFLINE:  # 离线状态
                # 离线状态，登陆账号
                username_element = ""
                password_element = ""
                login_element = ""

                ret, cookies = self._browser.login(self.account_info, self.loginUrl, username_element, password_element,
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
                            # logging.info("进入和cookies{}".format(cookies))
                            logging.info("进入登录状态,cookie已经获取")
                            return True, cookies
                        else:
                            logging.error("账号没有cookie不可用")
                            self.account_info.clear()
                            return False, ''
                    elif state[0] == AccountLoginStatus.PASSWORD_ERROR:  # 密码错误
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

    # 开始发帖
    def spider_post_list(self, post_url, title, pic_urls, content):
        print("spider_post_list 发帖开始")
        try:
            print(title, content)
            time.sleep(random.randint(2, 3))
            logging.info(u"开始论坛发帖，主页URL：{}".format(post_url))
            status = self._browser.open_link(post_url, title, pic_urls, content)
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
        # """
        # 启动浏览器，登陆僵尸账号
        # :return: 成功，返回True；失败，返回False
        # """
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
        # 社区
        community = "r/maxin8556"
        title = "圣人语录<一>"
        # pic_urls = ["/root/mx/AccountForum/picture/a.jpg",
        #             "/root/mx/AccountForum/picture/b.jpg"]
        pic_urls = [r"D:\MaXin-Study\2021-10-3\FinalVersionAccountForum\picture\a.jpg",
                    r"D:\MaXin-Study\2021-10-3\FinalVersionAccountForum\picture\b.jpg"]
        video_urls = ""
        content = "志坚者,功名之柱也。登山不以艰险而止,则必臻乎峻岭"

        # else:
        #     logging.error("论坛发帖过程没有发帖内容错误")
        #     return False

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
    t1 = time.time()
    spider = SkyscraperSpiderTest()
    # path = r"D:\MaXin-Study\2021-10-3\FinalVersionAccountForum\cookieData\cookiematters\cookies-maxin8556@163.com.json"
    path = ""
    account_info = ""
    print(spider.run(path, account_info))
    print('耗时:', time.time() - t1)
