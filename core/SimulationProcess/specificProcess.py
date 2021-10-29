#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from selenium.webdriver.support.select import Select

sys.path.append("../")

from selenium import webdriver
from core.SpiderRetCode import SelenRetCode
from core.SimulationProcess.FBSimulateProcess import FBSimulateProcess
import time
import random
import logging
import logging.config
from selenium import common
from selenium.webdriver.support.wait import WebDriverWait
from core.FBInfoDef import FBRetCode
from core.elementLocation import TumblrElement, RedditElement, BloggerElement, MattersElement, YorkbbsElement, \
    SkyscraperElement, KomicaElement, PixnetElement, ShowweElement, UlifestyleElement, NybbsElement,HtcElement

"""各个站点----具体流程(登录,发帖等)"""

# Htc 网站
class Htc(FBSimulateProcess):

    # 启动浏览器 ---配置浏览器设置
    def open(self):
        """Open browser."""
        return self.__open_browser()

    # 配置浏览器设置
    def __open_browser(self):
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

            # chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）

            # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            # chrome_options.add_argument('--disable-popup-blocking')  # 禁用javascript
            # ================
            # chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
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
    # Htc 发帖========修改发帖元素
    def open_link(self, post_url, title, media_urls, content):
        try:
            self.driver.get(post_url)

            # time.sleep(random.randint(1, 3))
            time.sleep(15)

            # 判断是否进入发帖页面
            if not self.driver.find_element_by_id(HtcElement.htc_post['title_id']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE

            # 先选择发布类别
            self.driver.find_element_by_xpath('//*[@id="postform"]/div[1]/div/button').click()
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="category"]/li[1]').click()
            time.sleep(3)


            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_id(HtcElement.htc_post['title_id']))

            title_input.send_keys(title)
            time.sleep(0.5)
            logging.info("标题输入完成")


            # 内容
            # 内容
            self.driver.switch_to.frame('e_iframe')
            if len(content) < 15:
                # print("内容需要大于15个字")
                WebDriverWait(self.driver, 20).until(
                    lambda driver:driver.find_element_by_xpath(HtcElement.htc_post['text_xpath'])).send_keys(content)
                logging.info('内容需要大于15个字')
            else:
                WebDriverWait(self.driver, 20).until(
                    lambda driver: driver.find_element_by_xpath(HtcElement.htc_post['text_xpath'])).send_keys(str(content+"                "))
            self.driver.switch_to.default_content()

            if media_urls:
                # 点击图片按钮
                image_click1 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                    driver.find_element_by_xpath(
                                                                        HtcElement.htc_post[
                                                                            'imageClick1_xpath']))
                image_click1.click()
                time.sleep(2)
                if len(media_urls) == 1:
                    media_url1 = media_urls[0]
                    # 图片发送
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_xpath(
                                                                           HtcElement.htc_post[
                                                                               'imageInput1_xpath']))
                    image_input.send_keys(media_url1)
                    time.sleep(2)
                    # 点击上传按钮
                    image_click2 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                        driver.find_element_by_xpath(
                                                                            HtcElement.htc_post[
                                                                                'imageClick2_xpath']))
                    image_click2.click()
                    time.sleep(3)
                    # 上传图片
                    image_post = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                      driver.find_element_by_xpath(
                                                                          HtcElement.htc_post[
                                                                              'imagePost1_xpath']))
                    image_post.click()
                    time.sleep(3)
                elif len(media_urls) == 2:
                    media_url1 = media_urls[0]
                    media_url2 = media_urls[1]
                    # 图片发送
                    image_input1 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_xpath(
                                                                           HtcElement.htc_post[
                                                                               'imageInput1_xpath']))
                    image_input1.send_keys(media_url1)
                    time.sleep(4)
                    image_input2 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                        driver.find_element_by_xpath(
                                                                            HtcElement.htc_post[
                                                                                'imageInput2_xpath']))
                    image_input2.send_keys(media_url2)
                    time.sleep(5)
                    # 点击上传按钮
                    image_click2 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                        driver.find_element_by_xpath(
                                                                            HtcElement.htc_post[
                                                                                'imageClick2_xpath']))
                    image_click2.click()
                    time.sleep(7)
                    # 上传图片
                    image_post1 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                      driver.find_element_by_xpath(
                                                                          HtcElement.htc_post[
                                                                              'imagePost1_xpath']))
                    image_post1.click()
                    time.sleep(3)
                    image_post2 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_xpath(
                                                                           HtcElement.htc_post[
                                                                               'imagePost2_xpath']))
                    image_post2.click()
                    time.sleep(3)
                logging.info("图片输入完成")

            # 点击勾选接受协议
            self.driver.find_element_by_xpath('//*[@id="agreerule"]').click()
            time.sleep(3)


            # 点击发送
            post_button = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   HtcElement.htc_post['post_xpath']))
            time.sleep(2)
            post_button.click()
            time.sleep(5)
            # driver.current_url方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))
            if current_url == "https://community.htc.com/tw/chat.php?mod=post&action=newthread&fid=77&extra=&topicsubmit=yes":
                logging.info("两次发帖需要间隔600秒")
                return FBRetCode.OTHER_ERROR
            else:
                logging.info(u'账号发帖完成')
                return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR

# nybbs 网站
class Nybbs(FBSimulateProcess):
    # Nybbs 发帖========修改发帖元素
    def open_link(self, post_url, title, media_urls, content):
        try:
            self.driver.get(post_url)

            time.sleep(random.randint(1, 3))

            # 判断是否进入发帖页面
            if not self.driver.find_element_by_name(NybbsElement.nybbs_post['title_name']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE


            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_name(
                                                                   NybbsElement.nybbs_post['title_name']))

            title_input.send_keys(title)
            time.sleep(0.5)
            logging.info("标题输入完成")


            # 内容
            # 进入iframe
            self.driver.switch_to.frame('e_iframe')
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   NybbsElement.nybbs_post['text_xpath']))

            content_input.send_keys(content)
            time.sleep(1)
            logging.info("内容输入完成")
            # 退出iframe
            self.driver.switch_to.default_content()



            if media_urls:
                # for media_url in media_urls:
                if len(media_urls) == 1:
                    media_url1 = media_urls[0]
                    # 点击图片按钮
                    image_click1 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_id(
                                                                           NybbsElement.nybbs_post[
                                                                               'image_click1_id']))
                    image_click1.click()
                    time.sleep(2)
                    # 上传图片
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                        driver.find_element_by_name(
                                                                            NybbsElement.nybbs_post[
                                                                                'imageInput_name']))
                    image_input.send_keys(media_url1)
                    time.sleep(2)
                    # 点击图片上传
                    image_post = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                        driver.find_element_by_xpath(
                                                                            NybbsElement.nybbs_post[
                                                                                'imagePost1_xpath']))
                    image_post.click()

                    logging.info("图片输入完成")
                elif len(media_urls) == 2:
                    media_url1 = media_urls[0]
                    media_url2 = media_urls[1]
                    # 点击图片按钮
                    image_click1 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                        driver.find_element_by_id(
                                                                            NybbsElement.nybbs_post[
                                                                                'image_click1_id']))
                    image_click1.click()
                    time.sleep(2)
                    # 上传图片
                    image_input1 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_name(
                                                                           NybbsElement.nybbs_post[
                                                                               'imageInput_name']))
                    image_input1.send_keys(media_url1)
                    time.sleep(5)
                    # 上传图片
                    image_input2 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                        driver.find_element_by_name(
                                                                            NybbsElement.nybbs_post[
                                                                                'imageInput_name']))
                    image_input2.send_keys(media_url2)
                    time.sleep(4)
                    # 点击图片上传
                    image_post = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                      driver.find_element_by_xpath(
                                                                          NybbsElement.nybbs_post[
                                                                              'imagePost1_xpath']))
                    image_post.click()
                    time.sleep(2)
                    # 点击图片上传
                    image_post = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                      driver.find_element_by_xpath(
                                                                          NybbsElement.nybbs_post[
                                                                              'imagePost2_xpath']))
                    image_post.click()
                    time.sleep(2)
                    logging.info("图片输入完成")


            # 点击发送
            post_button = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_id(
                                                                   NybbsElement.nybbs_post['post_id']))
            time.sleep(2)
            post_button.click()

            time.sleep(5)
            # driver.current_url方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')
            return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR

# Showwe 网站
class Showwe(FBSimulateProcess):
    # Komica 发帖========修改发帖元素
    def open_link(self, post_url, title, media_urls, content):
        try:
            self.driver.get(post_url)

            time.sleep(random.randint(1, 3))

            # 判断是否进入发帖页面
            if not self.driver.find_element_by_name(ShowweElement.showwe_element['title_name']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE


            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_name(
                                                                   ShowweElement.showwe_element['title_name']))

            title_input.send_keys(title)
            time.sleep(0.5)
            logging.info("标题输入完成")

            # 点击选择分类
            opt = self.driver.find_element_by_name('ctl00$c1$ddlCate')
            # 选择分类
            Select(opt).select_by_index(3)

            # 文章摘要

            article_abstract = self.driver.find_element_by_name('ctl00$c1$txtSummary')
            if len(title) < 10:
                article_abstract.send_keys(title + "          ")
            else:
                article_abstract.send_keys(title)

            # 内容
            # 进入iframe
            self.driver.switch_to.frame('txtTinymce_ifr')
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   ShowweElement.showwe_element['text_xpath']))

            content_input.send_keys(content)
            time.sleep(1)
            logging.info("内容输入完成")
            # 退出iframe
            self.driver.switch_to.default_content()



            if media_urls:
                for media_url in media_urls:
                    # 图片
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_name(
                                                                           ShowweElement.showwe_element[
                                                                               'image_name']))
                    image_input.send_keys(media_url)
                    time.sleep(2)
                    logging.info("图片输入完成")


            # 点击发送
            post_button = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_name(
                                                                   ShowweElement.showwe_element['post_name']))
            time.sleep(2)
            post_button.click()

            time.sleep(5)
            # driver.current_url方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')
            return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR


# Pixnet 网站
class Pixnet(FBSimulateProcess):

    # 启动浏览器 ---配置浏览器设置
    def open(self):
        """Open browser."""
        return self.__open_browser()

    # 配置浏览器设置
    def __open_browser(self):
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

            # chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）

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

    # Pixnet 发帖========修改发帖元素
    def open_link(self, post_url, title, media_urls, content):
        try:
            self.driver.get(post_url)
            time.sleep(5)
            # 点击发帖页面
            self.driver.find_element_by_xpath(PixnetElement.pixnet_element['goPost_xpath']).click()

            time.sleep(random.randint(1, 3))

            # 判断是否进入发帖页面
            if not self.driver.find_element_by_id(PixnetElement.pixnet_element['title_id']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE

            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_id(
                                                                   PixnetElement.pixnet_element['title_id']))

            title_input.send_keys(title)
            time.sleep(3)
            logging.info("标题输入完成")

            # 文本
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_id(
                                                                     PixnetElement.pixnet_element['text_id']))
            content_input.send_keys(content)
            time.sleep(4)
            logging.info("内容输入完成")


            if media_urls:
                for media_url in media_urls:
                    # 图片
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_xpath(
                                                                           PixnetElement.pixnet_element[
                                                                               'image_xpath']))
                    image_input.send_keys(media_url)
                    time.sleep(2)
                    logging.info("图片输入完成")

            time.sleep(4)
            post_button = WebDriverWait(self.driver, 30).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   PixnetElement.pixnet_element['post_xpath']))
            time.sleep(2)
            post_button.click()

            time.sleep(8)
            # driver.current_url方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')
            return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR


# Komica 网站
class Komica(FBSimulateProcess):
    # Komica 发帖========修改发帖元素
    def open_link(self, post_url, title, media_urls, content, username, password):
        try:
            self.driver.get(post_url)


            time.sleep(random.randint(1, 3))

            # 判断是否进入发帖页面
            if not self.driver.find_element_by_id(KomicaElement.Komica_post['title_id']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE

            # 名称
            name_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_id(
                                                                   KomicaElement.Komica_post['name_id']))
            name_input.send_keys(username)
            time.sleep(3)

            # emali
            password_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                              driver.find_element_by_id(
                                                                  KomicaElement.Komica_post['password_id']))
            password_input.send_keys(password)


            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_id(
                                                                   KomicaElement.Komica_post['title_id']))

            title_input.send_keys(title)
            time.sleep(3)
            logging.info("标题输入完成")

            if media_urls:
                for media_url in media_urls:
                    # 图片
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_xpath(
                                                                           KomicaElement.Komica_post[
                                                                               'image_xpath']))
                    image_input.send_keys(media_url)
                    time.sleep(2)
                    logging.info("图片输入完成")

            # 文本
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_xpath(
                                                                     KomicaElement.Komica_post['text_xpath']))
            content_input.send_keys(content)
            time.sleep(3)
            logging.info("内容输入完成")

            post_button = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_name(
                                                                   KomicaElement.Komica_post['post_name']))
            time.sleep(3)
            post_button.click()

            time.sleep(5)
            # driver.current_url方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')
            return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR


# Matters 网站
class Matters(FBSimulateProcess):

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
            logging.info("开始登录")
            # 该网站封IP比较厉害,必须要有间隔时间
            # 该网站点击登录按钮
            go_Login = MattersElement.matters_login['goLogin_xpath']
            go_Login_click = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                  driver.find_element_by_xpath(
                                                                      go_Login))
            time.sleep(1)
            go_Login_click.click()
            time.sleep(2)
            # 输入账号
            username_element = MattersElement.matters_login['username_xpath']
            account_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_xpath(
                                                                     username_element))

            account_input.send_keys(account_info.get("account"))
            time.sleep(7)
            # 有验证码

            # 输入密码
            password_element = MattersElement.matters_login['password_xpath']
            account_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_xpath(
                                                                     password_element))

            account_input.send_keys(account_info.get("password"))
            time.sleep(5)

            # 点击登录
            login_element = MattersElement.matters_login['Longin_xpath']
            login_click = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   login_element))
            login_click.click()
            time.sleep(5)
            # 获取cookie
            cookie = self.driver.get_cookies()

            logging.info(u'账号登录完成，用户=【{}】'.format(account_info.get("account")))
            self.driver.get_screenshot_as_file(r'/root/mx/AccountForum/picture/{}Login.png'.format(web_source))

            time.sleep(5)



            return SelenRetCode.SUCCESS, cookie
        except Exception as msg:
            logging.exception(u"账号登录异常，异常信息：{}".format(msg))
            self.__close_browser()
            return SelenRetCode.BROWSER_ERROR
        finally:
            time.sleep(random.randint(1, 2))

    # Matters 发帖   # 这里比较特殊,需要直接点击发帖按钮,发布帖子链接(post)在变化
    def open_link(self, post_url, title, media_urls, content):
        try:
            # 点击进入发帖页面
            self.driver.find_element_by_xpath(MattersElement.matters_post_element['goPost_xpath']).click()

            time.sleep(10)

            # 判断是否进入发帖页面(判断是否有标题元素)
            if not self.driver.find_element_by_xpath(MattersElement.matters_post_element['title_xpath']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE

            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   MattersElement.matters_post_element[
                                                                       'title_xpath']))

            title_input.send_keys(title)
            time.sleep(5)
            logging.info("标题输入完成")

            # 图片
            if media_urls:
                # 这里需要点击工具栏按钮
                image_click = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                   driver.find_element_by_xpath(
                                                                       MattersElement.matters_post_element[
                                                                           'image_click1_xpath']))
                time.sleep(1)
                image_click.click()
                for media_url in media_urls:
                    # 上传图片
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_xpath(
                        MattersElement.matters_post_element[
                            'image_xpath']))
                    image_input.send_keys(media_url)
                    time.sleep(2)
                    logging.info("标题输入完成")

            # 文本
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_xpath(
                                                                     MattersElement.matters_post_element[
                                                                         'text_xpath']))

            content_input.send_keys(content)
            time.sleep(2)
            logging.info("内容输入完成")

            # 点击发送按钮 发送帖子
            self.driver.find_element_by_xpath(MattersElement.matters_post_element['post_xpath']).click()
            time.sleep(2)
            # 发布之后确定发布
            self.driver.find_element_by_xpath(MattersElement.matters_post_element['confirmPost_xpath']).click()
            time.sleep(2)
            # 确认发布之后,再次点击发布
            self.driver.find_element_by_xpath(MattersElement.matters_post_element['againConfirm_xpath']).click()

            # 必须要查看自己的作品,要不然发不出去
            self.driver.find_element_by_xpath(MattersElement.matters_post_element['see_click']).click()

            # 方法可以得到当前页面的URL
            time.sleep(3)
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')

            return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR


# Blogger 网站
class Blogger(FBSimulateProcess):

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
            time.sleep(20)

            # 账号
            username_element = BloggerElement.blogger_login['username_name']
            account_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_name(
                                                                     username_element))
            account_input.send_keys(account_info.get("account"))
            time.sleep(5)

            # 点击下一步
            next_element = BloggerElement.blogger_login['next_class']
            next_click = WebDriverWait(self.driver, 20).until(lambda driver:
                                                              driver.find_element_by_class_name(
                                                                  next_element))
            time.sleep(1)
            next_click.click()
            # 这里需要输入验证码
            time.sleep(30)
            # 密码
            password_element = BloggerElement.blogger_login['password_name']
            password_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                  driver.find_element_by_name(password_element))
            password_input.send_keys(account_info.get("password"))
            time.sleep(5)

            # 点击登录
            login_element = BloggerElement.blogger_login['Longin_class']
            submit = WebDriverWait(self.driver, 20).until(lambda driver:
                                                          driver.find_element_by_class_name(
                                                              login_element))
            submit.click()
            time.sleep(5)

            # 获取cookie
            cookie = self.driver.get_cookies()

            logging.info(u'账号登录完成，用户=【{}】'.format(account_info.get("account")))

            time.sleep(10)

            return SelenRetCode.SUCCESS, cookie
        except Exception as msg:
            logging.exception(u"账号登录异常，异常信息：{}".format(msg))
            self.__close_browser()
            return SelenRetCode.BROWSER_ERROR
        finally:
            time.sleep(random.randint(1, 2))

    # Blogger 发帖   # 这里比较特殊,需要直接点击发帖按钮,发布帖子链接(post)在变化
    def open_link(self, post_url, title, media_urls, content):
        try:
            time.sleep(random.randint(1, 3))

            # 点击发布按钮
            goPost_click = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                driver.find_element_by_class_name(
                                                                    BloggerElement.blogger_post_element[
                                                                        'go_post_class']))

            goPost_click.click()
            time.sleep(10)

            # 进入发帖页面
            # 判断是否进入发帖页面(判断是否有标题元素)
            if not self.driver.find_element_by_class_name(BloggerElement.blogger_post_element['title_class']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE

            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_class_name(
                                                                   BloggerElement.blogger_post_element['title_class']))

            title_input.send_keys(title)
            time.sleep(2)
            logging.info("标题输入完成")
            # 文本
            # 进入iframe
            textIframe = self.driver.find_elements_by_xpath('//iframe')[1]
            self.driver.switch_to.frame(textIframe)
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_xpath(
                                                                     BloggerElement.blogger_post_element[
                                                                         'text_xpath']))

            content_input.send_keys(content)
            time.sleep(2)
            logging.info("内容输入完成")
            # 退出iframe
            self.driver.switch_to.default_content()

            # 图片
            if media_urls:
                # 图片
                # 先点击图片按钮
                image_click1 = self.driver.find_elements_by_class_name(
                    BloggerElement.blogger_post_element['imageClick_class'])[5]

                time.sleep(1)
                image_click1.click()

                # 点击从电脑选择
                image_click2 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                    driver.find_element_by_xpath(
                                                                        BloggerElement.blogger_post_element[
                                                                            'imageClick_xpath2']))
                time.sleep(3)
                image_click2.click()

                time.sleep(7)
                # 进入iframe页面
                imageIframe = self.driver.find_elements_by_xpath('//iframe')[4]

                self.driver.switch_to.frame(imageIframe)
                # 有多张图片循环上传
                for media_url in media_urls:
                    # 发送图片
                    image_click3 = self.driver.find_element_by_xpath(
                        BloggerElement.blogger_post_element['imageClick_xpath3'])

                    image_click3.send_keys(media_url)
                    time.sleep(8)
                # 点击发送图片按钮
                image = self.driver.find_element_by_xpath(BloggerElement.blogger_post_element['image_xpath'])
                time.sleep(1)
                image.click()
                # 给图片上传时间
                time.sleep(5)
                logging.info("图片输入完成")
                # 退出iframe
                self.driver.switch_to.default_content()

            # 点击发布
            post_click = self.driver.find_element_by_xpath(BloggerElement.blogger_post_element['post_xpath'])
            time.sleep(2)
            post_click.click()

            # 再次点击确定发布
            self.driver.find_element_by_xpath(BloggerElement.blogger_post_element['definePost_xpath']).click()

            time.sleep(3)
            # 方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')

            return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR


# reddit 网站
class Reddit(FBSimulateProcess):

    # 启动浏览器 ---配置浏览器设置
    def open(self):
        """Open browser."""
        return self.__open_browser()

    # 配置浏览器设置
    def __open_browser(self):
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
            # chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
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

    # reddit 发帖========修改发帖元素
    def open_link(self, post_url, title, media_urls, content):
        try:
            self.driver.get(post_url)
            time.sleep(random.randint(1, 3))
            # 发帖图片
            # self.driver.get_screenshot_as_file('../picture/redditPostPictures.png')

            # 判断是否进入发帖页面(判断是否有标题元素)
            if not self.driver.find_element_by_xpath(RedditElement.reddit_element['title']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE

            # 社区
            community_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   RedditElement.reddit_element['Community']))
            community_input.send_keys("u/BeataBecky")
            time.sleep(0.5)

            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   RedditElement.reddit_element['title']))

            title_input.send_keys(title)
            time.sleep(0.5)
            logging.info("标题输入完成")

            # 文本
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_xpath(
                                                                     RedditElement.reddit_element['text']))
            content_input.send_keys(content)
            logging.info("文本输入完成")

            if media_urls:
                for media_url in media_urls:
                    # 图片
                    # 文本
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_xpath(
                                                                           RedditElement.reddit_element[
                                                                               'image']))
                    image_input.send_keys(media_url)
                    time.sleep(2)
                    logging.info("图片输入完成")

            time.sleep(7)
            self.driver.find_element_by_xpath(RedditElement.reddit_element['post']).click()
            time.sleep(5)
            # 方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')

            if post_url in current_url:
                return FBRetCode.REPEAT_FAILD
            else:
                return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            return FBRetCode.OTHER_ERROR


# Tumblr 网站
class Tumblr(FBSimulateProcess):
    # tumblr 发帖========修改发帖元素
    def open_link(self, post_url, title, media_urls, content):
        try:
            self.driver.get(post_url)

            # page_source = self.driver.page_source
            # with open('login_error.html', 'w',encoding='utf8') as f:
            #     f.write(page_source)

            time.sleep(random.randint(1, 3))
            # 发帖图片
            # self.driver.get_screenshot_as_file('../picture/tumblrPostPictures.png')

            # 进入iframe标签
            frameXpath = '//*[@id="base-container"]/div[4]/div/iframe'
            # 判断是否进入发帖页面
            if not self.driver.find_element_by_xpath(frameXpath):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE

            frame = self.driver.find_element_by_xpath(frameXpath)
            # 进入 frame页面
            self.driver.switch_to.frame(frame)

            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   TumblrElement.tumblr_element['title']))

            title_input.send_keys(title)
            time.sleep(0.5)
            logging.info("标题输入完成")

            if media_urls:
                for media_url in media_urls:
                    # 图片
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                       driver.find_element_by_xpath(
                                                                           TumblrElement.tumblr_element[
                                                                               'image']))
                    image_input.send_keys(media_url)
                    time.sleep(2)
                    logging.info("图片输入完成")

            # 文本
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_xpath(
                                                                     TumblrElement.tumblr_element['text']))
            content_input.send_keys(content)
            time.sleep(7)
            logging.info("内容输入完成")

            # self.driver.get_screenshot_as_file(r'/root/mx/AccountForum/picture/click.png')
            # self.driver.find_element_by_xpath(TumblrElement.tumblr_element['post']).click()
            post_button = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   TumblrElement.tumblr_element['post']))
            time.sleep(5)
            post_button.click()
            # element = self.driver.find_element_by_xpath(TumblrElement.tumblr_element['post'])
            # self.driver.execute_script("arguments[0].click();", element)

            time.sleep(3)
            # driver.current_url方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')

            if post_url in current_url:
                return FBRetCode.REPEAT_FAILD
            else:
                return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR


# ForumYorkbbs 网站
class ForumYorkbbs(FBSimulateProcess):
    # ForumYorkbbs 发贴
    def open_link(self, post_url, title, media_urls, content):
        try:

            self.driver.get(post_url)
            time.sleep(random.randint(1, 3))
            # 检测有没有登录成功
            if not self.driver.find_elements_by_xpath(YorkbbsElement.activity_xpath['account_xpath']):
                logging.error("cookie失效或者浏览器没有加载上cookie")
                return FBRetCode.LINK_OVERDUE
            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_id(
                                                                   YorkbbsElement.activity_xpath['text_title_xpath']))
            title_input.send_keys(title)
            time.sleep(0.5)
            logging.info("标题输入完成")

            # 定位到iframe
            iframe = self.driver.find_element_by_id(YorkbbsElement.activity_xpath['button_iframe_xpath'])
            # 切换到iframe
            self.driver.switch_to_frame(iframe)
            content_input = WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element_by_id(YorkbbsElement.activity_xpath['text_content_xpath']))
            content_input.send_keys(content)
            logging.info("内容输入完成")
            # 退出iframe
            self.driver.switch_to.default_content()

            if media_urls:
                for media_url in media_urls:
                    # 图片
                    submit1 = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id(
                        YorkbbsElement.activity_xpath['click_pic']))
                    submit1.click()
                    time.sleep(2)
                    submit2 = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id(
                        YorkbbsElement.activity_xpath['click_pic_next']))
                    submit2.click()
                    time.sleep(2)
                    # 定位到iframe
                    iframe = self.driver.find_element_by_id(YorkbbsElement.activity_xpath['button_iframe_media_xpath'])
                    # 切换到iframe
                    self.driver.switch_to_frame(iframe)
                    submit3 = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                   driver.find_element_by_id(
                                                                       YorkbbsElement.activity_xpath['post_pic']))
                    submit3.send_keys(media_url)
                    logging.info("图片输入完成")
                    # 退出iframe
                    self.driver.switch_to.default_content()
                    time.sleep(5)

            submit = WebDriverWait(self.driver, 20).until(lambda driver:
                                                          driver.find_element_by_id(
                                                              YorkbbsElement.activity_xpath['button_post_xpath']))
            submit.click()
            logging.info(u'账号发帖完成')
            time.sleep(5)
            # current_url 方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))
            if post_url in current_url:
                return FBRetCode.REPEAT_FAILD
            else:
                return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            return FBRetCode.OTHER_ERROR



# Ulifestyle 网站
class Ulifestyle(FBSimulateProcess):
    # Ulifestyle 发帖========修改发帖元素
    def open_link(self, post_url, title, media_urls, content):
        try:
            self.driver.get(post_url)
            time.sleep(random.randint(1, 3))
            # 判断是否进入发帖页面
            if not self.driver.find_element_by_id(UlifestyleElement.ulifestyle_element['title_id']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE

            # 这里需要点击那个cookie改善网站体验
            cookie_click = self.driver.find_element_by_xpath('//*[@id="cookies-notification"]/div/div[2]')
            cookie_click.click()



            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_id(
                                                                   UlifestyleElement.ulifestyle_element['title_id']))

            title_input.send_keys(title)
            time.sleep(3)
            logging.info("标题输入完成")

            # 内容
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   UlifestyleElement.ulifestyle_element['text_xpath']))

            content_input.send_keys(content)
            time.sleep(3)
            logging.info("内容输入完成")



            if media_urls:
                for media_url in media_urls:
                    # 这里需要用js把图片input标签的隐藏属性重写
                    js = "document.getElementById(\"upload-post-photo\").style.display='block';"
                    self.driver.execute_script(js)
                    time.sleep(1)
                    image_input = self.driver.find_element_by_id("upload-post-photo")
                    time.sleep(0.5)
                    image_input.send_keys(media_url)
                    time.sleep(2)
                    logging.info("图片输入完成")

            # 点击发布
            post_button = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   UlifestyleElement.ulifestyle_element['post_xpath']))
            time.sleep(2)
            post_button.click()

            # 发布之后需要点击发布分类
            time.sleep(3)
            classify = self.driver.find_element_by_xpath(UlifestyleElement.ulifestyle_element['classify_xpath'])
            time.sleep(2)
            classify.click()
            time.sleep(2)
            # 点击分类之后需要点击预览文章
            self.driver.find_element_by_xpath('//*[@id="app"]/div[3]/div/div[3]/div/button').click()
            time.sleep(5)
            # 预览文章之后点击发送--->发送成功
            # 点击发布
            self.driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[1]/div/div/button').click()
            # self.driver.find_element_by_class_name('previewNav__actions-publish').click()

            time.sleep(20)
            # driver.current_url方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))
            if current_url == post_url:
                logging.info("发布失败")
                return FBRetCode.OTHER_ERROR
            else:
                logging.info(u'账号发帖完成')
                return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR


# SkyscraperCity 网站
class Skyscrapercity(FBSimulateProcess):

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
            logging.info("开始登录")
            # 该网站封IP比较厉害,必须要有间隔时间
            # 该网站点击登录按钮
            go_Login = SkyscraperElement.skyscraper_login['goLogin_xpath']
            go_Login_click = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                  driver.find_element_by_xpath(
                                                                      go_Login))
            time.sleep(5)
            go_Login_click.click()
            time.sleep(5)
            # 输入账号
            username_element = SkyscraperElement.skyscraper_login['username_name']
            account_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_name(
                                                                     username_element))
            time.sleep(2)
            account_input.send_keys(account_info.get("account"))
            time.sleep(6)

            # 输入密码
            password_element = SkyscraperElement.skyscraper_login['password_name']
            account_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_name(
                                                                     password_element))
            time.sleep(4)
            account_input.send_keys(account_info.get("password"))
            time.sleep(5)

            # 点击登录
            login_element = SkyscraperElement.skyscraper_login['Longin_xpath']
            login_click = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_xpath(
                                                                   login_element))
            login_click.click()
            time.sleep(5)
            # 获取cookie
            cookie = self.driver.get_cookies()

            logging.info(u'账号登录完成，用户=【{}】'.format(account_info.get("account")))

            time.sleep(5)

            return SelenRetCode.SUCCESS, cookie
        except Exception as msg:
            logging.exception(u"账号登录异常，异常信息：{}".format(msg))
            self.__close_browser()
            return SelenRetCode.BROWSER_ERROR
        finally:
            time.sleep(random.randint(1, 2))

    # SkyscraperCity 发帖
    def open_link(self, post_url, title, media_urls, content):
        try:
            # 点击进入发帖页面
            self.driver.get(post_url)

            time.sleep(10)
            # 判断是否进入发帖页面(判断是否有标题元素)
            if not self.driver.find_element_by_name(SkyscraperElement.skyscraper_post['title_name']):
                logging.error("发帖页面异常,登录失败")
                return FBRetCode.LINK_OVERDUE
            # 发帖页面如果上一次发帖失败,标题和内容都会留来

            # 标题
            title_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                               driver.find_element_by_name(
                                                                   SkyscraperElement.skyscraper_post[
                                                                       'title_name']))

            title_input.send_keys(title)
            time.sleep(5)
            logging.info("标题输入完成")

            # 文本
            content_input = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                 driver.find_element_by_xpath(
                                                                     SkyscraperElement.skyscraper_post[
                                                                         'text_xpath']))

            content_input.send_keys(content)
            time.sleep(2)
            logging.info("内容输入完成")

            # 图片
            if media_urls:
                # 这里需要点击工具栏按钮
                image_click = WebDriverWait(self.driver, 20).until(lambda driver:
                                                                   driver.find_element_by_xpath(
                                                                       SkyscraperElement.skyscraper_post[
                                                                           'image_xpath_click']))
                time.sleep(1)
                image_click.click()
                for media_url in media_urls:
                    # 上传图片
                    image_input = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_xpath(
                        SkyscraperElement.skyscraper_post[
                            'go_image_xpath']))
                    image_input.send_keys(media_url)
                    time.sleep(2)
                    logging.info("图片输入完成")

            # 点击发送按钮 发送帖子
            self.driver.find_element_by_xpath(SkyscraperElement.skyscraper_post['post_xpath']).click()
            time.sleep(2)

            # 方法可以得到当前页面的URL
            current_url = self.driver.current_url
            logging.info("当前页面{}".format(current_url))

            logging.info(u'账号发帖完成')

            return FBRetCode.SUCCESS

        except common.exceptions.SessionNotCreatedException:
            logging.error(u"浏览器链接已断开，需重启浏览器")
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR
        except Exception as msg:
            logging.exception(u"homepage 状态检测异常，异常信息：{}".format(msg))
            # self.__close_browser()
            return FBRetCode.OTHER_ERROR