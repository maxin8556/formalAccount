#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 7/12/21 1:57 PM
# @Author: kevin
# @File: SimulationProcess.py
# @Software: PyCharm

import sys

sys.path.append("../../")
import os
import time
import random
import json
import logging
import logging.config
from selenium import common
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from core.FBInfoDef import FBRetCode
from core.SpiderRetCode import SelenRetCode, BrowserState, AccountLoginStatus
from Utils.CookieOperation import addCookie
from Utils.getElementType import getElementType


class FBSimulateProcess(object):

    def __init__(self):
        self.driver = None

    # 配置浏览器设置
    def __open_browser(self):
        """
        启动浏览器
        :return: 成功，True
        """

        try:
            # 设置无界面模式浏览器启动
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--ignore-certificate-errors')  # 忽略https警告
            chrome_options.add_argument('--disable-cache')
            chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
            chrome_options.add_argument('--start-maximized')  # 浏览器最大化
            chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
            chrome_options.add_argument('log-level=3')  # info(default) = 0 warning = 1 LOG_ERROR = 2 LOG_FATAL = 3

            # chrome_options.add_argument('--user-agent=""')  # 设置请求头的User-Agent
            chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示

            chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）

            # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            # chrome_options.add_argument('--disable-popup-blocking')  # 禁用javascript
            # ================
            chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            # # ================
            chrome_options.add_argument('lang=en')
            # chrome_options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
            chrome_options.add_argument('-–disable-software-rasterizer')
            chrome_options.add_argument('--disable-extensions')

            logging.info("启动谷歌浏览器")
            logging.info(os.name)
            # windows
            if os.name == 'nt':
                # self.driver = WebDriverWait(webdriver, 30).until(
                #     lambda driver: driver.Chrome(executable_path='/home/xuxin/drivers/bin/chromedriver',
                #                                  chrome_options=chrome_options)
                # )
                self.driver = WebDriverWait(webdriver, 30).until(
                    lambda driver: driver.Chrome(chrome_options=chrome_options,
                                                 service_log_path=os.path.devnull)
                )

            else:
                # 注释掉--显示浏览器
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')

                try:
                    self.driver = WebDriverWait(webdriver, 30).until(
                        lambda driver: driver.Chrome(executable_path='/home/xuxin/drivers/bin/chromedriver',
                                                     chrome_options=chrome_options,
                                                     service_log_path=os.path.devnull)
                    )
                    # self.driver = WebDriverWait(webdriver, 30).until(
                    #     lambda driver: driver.Chrome(executable_path='/home/maxin/chromedriver',
                    #                                  chrome_options=chrome_options,
                    #                                  service_log_path=os.path.devnull)
                    # )

                except Exception as msg:
                    logging.exception(u"谷歌浏览器chrome启动异常，异常信息：{}".format(msg))
                    return False

            self.driver.implicitly_wait(5)
            logging.info(u"谷歌浏览器启动完成！")
            return SelenRetCode.SUCCESS
        except Exception as msg:
            logging.exception(u"谷歌浏览器启动异常，异常信息：{}".format(msg))
            return SelenRetCode.BROWSER_ERROR
        finally:
            time.sleep(random.randint(2, 3))

    # 启动浏览器 ---配置浏览器设置
    def open(self):
        """Open browser."""
        return self.__open_browser()

    # 截图
    def save_screenshot_as_file(self, eenshot_as_file):
        self.driver.get_screenshot_as_file(eenshot_as_file)

    # 关闭浏览器
    def __close_browser(self):
        """
        关闭浏览器
        :return:
        """
        try:
            logging.info(u"关闭浏览器!")
            if hasattr(self.driver, 'quit'):
                self.driver.quit()
                self.driver = None
        except Exception as msg:
            logging.exception(u"浏览器关闭异常，异常信息：{}".format(msg))
        finally:
            time.sleep(random.randint(5, 8))

    # Close browser
    def close(self):
        """Close browser."""
        self.__close_browser()

    def forum_post(self, title, content):
        """
        进入发帖元素
        :param title:
        :param content:
        :return:
        """
        print(title, content)
        fb_address = 'http://forum.yorkbbs.ca/login.aspx'
        try:
            # self.clear_cookies()
            self.driver.get(fb_address)

            account_input = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('title'))
            # account_input.send_keys(account_info.get("account"))
            account_input.send_keys(title)
            time.sleep(0.5)
            password_input = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('wysiwyg'))
            # password_input.send_keys(account_info.get("password"))
            password_input.send_keys(content)
            time.sleep(0.5)
            submit = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('postsubmit'))
            submit.click()
            logging.info(u'账号发帖完成')
            return SelenRetCode.SUCCESS
        except Exception as msg:
            logging.exception(u"账号登录异常，异常信息：{}".format(msg))
            self.__close_browser()
            return SelenRetCode.BROWSER_ERROR
        finally:
            time.sleep(random.randint(1, 2))

    def __down_scrollbar(self, max_down_times, check_bottom=False, down_limit=250):
        """
        下拉好友列表操作
        :param max_down_times: 最大下拉次数
        :return:
        """
        try:
            action_down = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_xpath("//body"))
            num_down = 1
            for i in range(max_down_times):
                logging.info(U'下滑操作，第{}次'.format(num_down))
                num_down += 1
                # action_down.send_keys(Keys.END)

                # js = "var q=document.documentElement.scrollTop=100000"
                # self.driver.execute_script(js)

                action_down.send_keys(Keys.END)

                time.sleep(random.randint(2, 3))

            # 检查列表底部
            # old_page = ""
            # if check_bottom:
            #     while not self.is_buttom() and self.is_change(old_page):
            #         if num_down > down_limit:
            #             logging.info(u"下滑操作超过最大下滑次数，退出下滑操作")
            #             break
            #         old_page = self.driver.page_source
            #         logging.info(U'下滑操作，第{}次'.format(num_down))
            #         num_down += 1
            #         action_down.send_keys(Keys.END)
            #         time.sleep(random.randint(1, 2))
        except Exception as msg:
            logging.exception(u"滑动条下拉异常，异常信息：{}".format(msg))

    def move_to_element(self, xpath):
        """
        检测元素是否存在
        :param xpath: css过滤路径
        :return: 存在，True
        """
        element = None
        try:
            elements = self.driver.find_elements_by_xpath(xpath)
            print(elements)
            print(len(elements))
            print(type(elements))
            n = 0
            # for element in elements[0:10]:
            for element in elements:
                n += 1
                print(n)
                time.sleep(random.randint(1, 3))
                ActionChains(self.driver).move_to_element(element).perform()
        except Exception as msg:
            logging.exception(u"元素锁定异常，异常信息：{}".format(msg))
        finally:
            return element

    def is_change(self, page_source):
        """
        检查页面是否有变化
        :param page_source:
        :return:
        """
        if page_source == self.driver.page_source:
            logging.info(u"内容刷新完成，终止下滑操作！")
            return False
        else:
            return True

    def is_buttom(self):
        """
        检测页面底部元素
        :return:
        """
        if self.check_element_by_xpath('//div[@class="_36d" and @id="timeline-medley"]'
                                       '/div/div[@id="pagelet_timeline_medley_photos"]'):
            logging.info(u"检测到好友列表底部元素，退出下滑操作")
            return True
        else:
            return False

    def check_element_by_xpath(self, element):
        """
        Xpath检查元素是否存在
        :param element:
        :return:
        """
        try:
            self.driver.find_element_by_xpath(element)
            return True
        except Exception:
            return False

    def is_element_exist(self, element):
        """
        检测元素是否存在
        :param element: css过滤路径
        :return: 存在，True
        """
        try:
            self.driver.find_element_by_css_selector(element)
            return True
        except Exception:
            return False

    def find_element_by_xpath(self, xpath):
        element = None
        try:
            element = WebDriverWait(self.driver, 30).until(
                lambda driver: driver.find_element_by_xpath(xpath)
            )
        except Exception as msg:
            logging.exception(u"元素锁定异常，异常信息：{}".format(msg))
        finally:
            return element

    def find_element_by_xpath_with_click(self, xpath):
        try:
            button_element = self.find_element_by_xpath(xpath)
            if button_element:
                button_element.click()
                time.sleep(random.randint(5, 8))
                logging.info(u"元素按钮锁定点击完成")
                return True
            else:
                logging.error(u"元素按钮所锁定失败")
                return False
        except Exception as msg:
            logging.exception(u"元素锁定点击异常，异常信息：{}".format(msg))
            self.save_screenshot_as_file("click_error.png")
            return False

    # 清理浏览器Cookies缓存
    def clear_cookies(self):
        """
        清理浏览器Cookies缓存
        :return:
        """
        if self.driver:
            self.driver.delete_all_cookies()

    # 添加cookie
    def add_cookies(self):
        """
        添加cookie
        :return:
        """
        if self.driver:
            self.driver.add_cookie()

    def get_page_source(self):
        """
        获取页面源码
        :return:
        """
        return self.driver.page_source

    # element_type:元素类型,username_element:用户名元素, password_element:密码元素, login_element:登录按钮元素
    def login(self, account_info, login_url, username_element, password_element, login_element,web_source):
        # 判断账号格式是否正确
        if not isinstance(account_info, dict):
            logging.error(u"僵尸账号信息类型不匹配")
            return SelenRetCode.FORMAT_ERROR
        if not account_info.get("account") or not account_info.get("password"):
            logging.error(u"僵尸账号信息格式不匹配")
            return SelenRetCode.FORMAT_ERROR
        try:
            self.clear_cookies()
            self.driver.get(login_url)
            time.sleep(3)
            logging.info("开始登录")
            # 账号
            if username_element:
                # 获取元素的属性和值
                element_type, element = getElementType(username_element)
                logging.info("开始输入账号=====")
                if element_type == "xpath":
                    account_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                         driver.find_element_by_xpath(element))
                    account_input.send_keys(account_info.get("account"))
                    time.sleep(3)
                elif element_type == "id":
                    account_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                         driver.find_element_by_id(element))
                    account_input.send_keys(account_info.get("account"))
                    time.sleep(3)
                elif element_type == "class":
                    account_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                         driver.find_element_by_class_name(
                                                                             element))
                    account_input.send_keys(account_info.get("account"))
                    time.sleep(3)
                elif element_type == "name":
                    account_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                         driver.find_element_by_name(element))
                    account_input.send_keys(account_info.get("account"))
                    time.sleep(3)
                elif element_type == "css":
                    account_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                         driver.find_element_by_css_selector(
                                                                             element))
                    account_input.send_keys(account_info.get("account"))
                    time.sleep(3)
                logging.info("账号输入完成=====")
                # self.driver.get_screenshot_as_file(r'/root/mx/AccountForum/picture/{}username.png'.format(web_source))
            else:
                logging.info("没有账号元素-----")

            if password_element:
                # 获取元素的属性和值
                element_type, element = getElementType(password_element)
                logging.info("开始输入密码=====")
                if element_type == "xpath":
                    # 点击下一步
                    password_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                          driver.find_element_by_xpath(
                                                                              element))
                    password_input.send_keys(account_info.get("password"))
                    time.sleep(3)
                elif element_type == "id":
                    # 点击下一步
                    password_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                          driver.find_element_by_id(element))
                    password_input.send_keys(account_info.get("password"))
                    time.sleep(3)
                elif element_type == "class":
                    password_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                          driver.find_element_by_class_name(
                                                                              element))
                    password_input.send_keys(account_info.get("password"))
                    time.sleep(3)
                elif element_type == "name":
                    password_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                          driver.find_element_by_name(element))
                    password_input.send_keys(account_info.get("password"))
                    time.sleep(3)
                elif element_type == "css":
                    password_input = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                          driver.find_element_by_css_selector(
                                                                              element))
                    password_input.send_keys(account_info.get("password"))
                    time.sleep(3)
                logging.info("密码输入完成=====")
                # self.driver.get_screenshot_as_file(r'/root/mx/AccountForum/picture/{}password.png'.format(web_source))
            else:
                logging.info("没有密码元素-----")

            if login_element:
                # 获取元素的属性和值
                element_type, element = getElementType(login_element)
                if element_type == "xpath":
                    # 点击下一步
                    submit = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                  driver.find_element_by_xpath(
                                                                      element))
                    submit.click()
                    time.sleep(3)
                elif element_type == "id":
                    # 点击下一步
                    submit = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                  driver.find_element_by_id(str(element)))
                    submit.click()
                    time.sleep(3)
                elif element_type == "class":
                    submit = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                  driver.find_element_by_class_name(
                                                                      element))
                    submit.click()
                    time.sleep(3)
                elif element_type == "name":
                    submit = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                  driver.find_element_by_name(element))
                    submit.click()
                    time.sleep(3)
                elif element_type == "css":
                    submit = WebDriverWait(self.driver, 40).until(lambda driver:
                                                                  driver.find_element_by_css_selector(
                                                                      element))
                    submit.click()
                    time.sleep(3)
            else:
                logging.info("没有登录点击元素-----")

            # 获取cookie
            cookie = self.driver.get_cookies()
            # 获取登录之后的页面,判断BUG用的
            # self.driver.get_screenshot_as_file(r'/root/mx/AccountForum/picture/{}Login.png'.format(web_source))

            logging.info(u'账号登录完成，用户=【{}】'.format(account_info.get("account")))

            time.sleep(2)

            return SelenRetCode.SUCCESS, cookie
        except Exception as msg:
            logging.exception(u"账号登录异常，异常信息：{}".format(msg))
            self.__close_browser()
            return SelenRetCode.BROWSER_ERROR
        finally:
            time.sleep(random.randint(1, 2))

    # 判断初始账号状态,有cookie文件就注入cookie登录,然后判断是否登陆成功,   没有就需要登录
    def check_browser_status(self, path, account_info, url, is_on_element):
        try:
            # 判断是否有Cookie文件
            cookiePath = path
            result = os.path.exists(cookiePath)
            if result:
                try:
                    self.clear_cookies()
                    self.driver.get(url)
                    logging.info("开始注入cookie~~")
                    # 注入cookie
                    addCookie(cookiePath, self.driver)
                    time.sleep(2)
                    # 注入成功后再次刷新
                    self.driver.get(url)
                    time.sleep(5)

                    # 这里判断有没有一个元素,有就是登录成功

                    if is_on_element:
                        # 获取元素的属性和值
                        element_type, element = getElementType(is_on_element)
                        if element_type == "xpath":
                            self.driver.find_element_by_xpath(element)
                        if element_type == "id":
                            self.driver.find_element_by_id(element)
                        if element_type == "class":
                            self.driver.find_element_by_class_name(element)
                        if element_type == "name":
                            self.driver.find_element_by_name(element)
                        if element_type == "css":
                            self.driver.find_element_by_css_selector(element)

                    logging.info("cookie注入成功")
                    cookie_items = self.driver.get_cookies()
                    logging.info("账号处于登录状态，账户：{}".format(account_info.get("account")))
                    return BrowserState.TYPE_ONLINE, cookie_items
                except:
                    logging.info("cookie失效,需要重新登录")
                    logging.info("账号处于离线状态，账户：{}".format(account_info.get("account")))
                    return BrowserState.TYPE_OFFLINE, ''

            else:
                logging.info("没有Cookie文件~~")
                return BrowserState.TYPE_OFFLINE, ''


        except common.exceptions.SessionNotCreatedException:
            logging.error("浏览器链接已断开，需重新启动浏览器?")
            self.__close_browser()
            return BrowserState.TYPE_EXCEPTION, ''
        except Exception as msg:
            logging.exception("浏览器界面账号状态检测异常，异常信息：{}".format(msg))
            self.__close_browser()
            return BrowserState.TYPE_EXCEPTION, ''

    # 判断发帖前账号的登录状态,是否成功登录
    def check_account_status(self, account_info, is_on_element, web_source):

        logging.info('检测go_post开始=========================')

        try:
            # 这里判断有没有一个元素,有就是登录成功
            if is_on_element:
                # 获取元素的属性和值
                element_type, element = getElementType(is_on_element)
                if element_type == "xpath":
                    self.driver.find_element_by_xpath(element)
                if element_type == "id":
                    self.driver.find_element_by_id(element)
                if element_type == "class":
                    self.driver.find_element_by_class_name(element)
                if element_type == "name":
                    self.driver.find_element_by_name(element)
                if element_type == "css":
                    self.driver.find_element_by_css_selector(element)
                logging.info('检测go_post成功=========================')
                logging.info(u"账号处于登录状态，账户：{}".format(account_info.get("account")))
                return AccountLoginStatus.NORMAL
        # 账号登陆失败未知错误
        except:
            logging.error('账号登陆失败未知错误，账号：{}'.format(account_info.get("account")))
            self.driver.get_screenshot_as_file(r'/root/mx/AccountForum/picture/{}LoginError.png'.format(web_source))
            return AccountLoginStatus.UNKNOWN_ERROR
