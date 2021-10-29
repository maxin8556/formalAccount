import os
import time
import random
import logging
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class WebService:


    def __init__(self):

        self._logger = logging.getLogger()
        self._driver = None

    def _open_firefox(self, startup_homepage='http://www.baidu.com'):

        try:
            firefox_profile = webdriver.FirefoxProfile()

            # 设置启动页
            firefox_profile.set_preference('browser.startup.homepage', startup_homepage)
            firefox_profile.set_preference('browser.startup.page', '1')
            # 设置不加载图片、通知窗口
            firefox_profile.set_preference('permissions.default.image', 2)
            firefox_profile.set_preference('permissions.default.desktop-notification', 2)
            firefox_profile.set_preference('plugin.state.flash', 0)
            # 设置本地不缓存
            firefox_profile.set_preference('browser.cache.check_doc_frequency', 3)
            firefox_profile.set_preference('browser.cache.disk.enable', False)
            firefox_profile.set_preference('browser.cache.memory.enable', False)
            firefox_options = webdriver.FirefoxOptions()
            # if proxy:
            #     firefox_options.add_argument('--proxy-server={}'.format(proxy))

            logging.info("启动火狐浏览器")
            if os.name == 'nt':

                self._driver = WebDriverWait(webdriver, 30).until(
                     lambda driver: driver.Firefox(executable_path='./bin/geckodriver.exe',
                                                   firefox_profile=firefox_profile)
                )
            else:
                firefox_options.add_argument('--headless')
                self._driver = WebDriverWait(webdriver, 30).until(
                    lambda driver: driver.Firefox(executable_path='./bin/geckodriver',
                                                  firefox_profile=firefox_profile,
                                                  options=firefox_options,
                                                  service_log_path=os.path.devnull)
                )
            self._driver.implicitly_wait(30)
            self._logger.info(u"火狐浏览器启动完成！")
            time.sleep(random.randint(8, 15))
            return True
        except Exception as msg:
            self._logger.exception(u"火狐浏览器启动异常，异常信息：{}".format(msg))
            return False

    def _open_chrome(self, startup_homepage='http://www.baidu.com'):

        try:
            # 设置无界面模式浏览器启动
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--ignore-certificate-errors')  # 忽略https警告
            chrome_options.add_argument('--disable-cache')
            chrome_options.add_argument('--disable-gpu')      # 禁用GPU加速
            chrome_options.add_argument('--start-maximized')  # 浏览器最大化
            chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
            chrome_options.add_argument('log-level=3')   # info(default) = 0 warning = 1 LOG_ERROR = 2 LOG_FATAL = 3

            # chrome_options.add_argument('--user-agent=""')  # 设置请求头的User-Agent
            chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
            chrome_options.add_argument('--incognito')        # 隐身模式（无痕模式）
            # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            # chrome_options.add_argument('--disable-popup-blocking')  # 禁用javascript
            chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            chrome_options.add_argument('lang=en')
            # chrome_options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
            chrome_options.add_argument('-–disable-software-rasterizer')
            chrome_options.add_argument('--disable-extensions')

            # if proxy:
            #
            #     chrome_options.add_argument('--proxy-server=http://{}'.format(proxy))
            logging.info("启动谷歌浏览器")

            print(os.name)
            #windows
            if os.name == 'nt':

                self._driver = WebDriverWait(webdriver, 30).until(
                    lambda driver: driver.Chrome(executable_path='/home/xuxin/drivers/bin/chromedriver',
                                                 chrome_options=chrome_options)
                )

            else:

                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                try:
                    # self._driver = WebDriverWait(webdriver, 30).until(
                    #     lambda driver: driver.Chrome(chrome_options=chrome_options,
                    #                                  service_log_path=os.path.devnull)
                    # )
                    self._driver = WebDriverWait(webdriver, 30).until(
                        lambda driver: driver.Chrome(executable_path='/home/xuxin/drivers/bin/chromedriver',
                                                     chrome_options=chrome_options,
                                                     service_log_path=os.path.devnull)
                    )
                except Exception as e:
                    return False
            self._driver.implicitly_wait(15)
            self._logger.info(u"谷歌浏览器启动完成！")
            time.sleep(0.5)
            return True

        except Exception as msg:

            self._logger.exception(u"谷歌浏览器启动异常，异常信息：{}".format(msg))
            return False, "浏览器启动失败{}".format(msg)

    def _open(self, web="Chrome", startup_homepage='http://www.baidu.com'):

        if "Chrome" == web:

            return self._open_chrome(startup_homepage)

        elif "Firefox" == web:

            return self._open_firefox(startup_homepage)

        else:

            return False, "浏览器不存在"

    def _close(self, web="Chrome"):

        if "Chrome" == web:

            if isinstance(self._driver, webdriver.Chrome):

                self._driver.quit()
                self._driver = None

        elif "Firefox" == web:

            if isinstance(self._driver, webdriver.Firefox):
                self._driver.quit()
                self._driver = None

        else:

            if hasattr(self._driver, "quit"):
                self._driver.quit()
                self._driver = None
        self._logger.info("关闭浏览器")

    def get_cookies(self):

        if self._driver:

            try:

                return self._driver.get_cookies()

            except:

                return {}

        else:

            return {}

    def clear_cookies(self):

        """
        清理浏览器Cookies缓存
        :return:
        """
        if self._driver:

            self._driver.delete_all_cookies()

    def refresh(self):

        if self._driver:

            self._driver.refresh()
        time.sleep(random.randint(3, 5))

    def set_firefox_incognito_mode(self):

        action_element = WebDriverWait(self._driver, 20).until(lambda driver: driver.find_element_by_xpath("//body"))
        action_element.send_keys(Keys.CONTROL, Keys.SHIFT, 'p')

    def record_web_status(self, title, save_path=os.path.join(os.getcwd(), "records"), html_enable=False):

        if not os.path.exists(save_path):

            os.makedirs(save_path)
        self._driver.get_screenshot_as_file(os.path.join(
            save_path,
            'image_' + title + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
        ))

        if html_enable:

            with open(os.path.join(
                    save_path,
                    "html_" + title + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".html"
            ), "wb") as _w:
                _w.write(self._driver.page_source)

    def open_browser(self, startup_homepage="https://twitter.com"):

        """
        启动浏览器
        :param startup_homepage: 启动页面
        :param proxy: 代理
        :return: True, 成功；False, 失败
        """
        return self._open(startup_homepage=startup_homepage)

    def check_browser(self, current_url="https://twitter.com"):

        """
        检测当前页面
        :param current_url:
        :return:
        """
        if current_url in self._driver.current_url:

            self._logger.info("Twitter首页打开成功")
            return True

        return False

    def close_browser(self):

        self._close()

    def find_element_by_xpath(self, xpath, description="ELEMENT", exception=True, timeout=60):

        element = None
        try:
            element = WebDriverWait(self._driver, timeout).until(
                lambda driver: driver.find_element_by_xpath(xpath)
            )
        except TimeoutException:
            if exception:
                self._logger.error("{}锁定超时".format(description))
                self.record_web_status(description)
        except Exception as msg:
            self._logger.exception("{}锁定异常，异常信息：{}".format(description, msg))
            self.record_web_status(description)
        finally:
            return element

    def find_element_by_xpath_with_click(self, xpath, description="BUTTON"):

        try:
            button_element = self.find_element_by_xpath(xpath, description)
            if button_element:
                button_element.click()
                time.sleep(random.randint(2, 3))
                self._logger.info("{}按钮点击完成".format(description))
                return button_element
            else:
                self._logger.error("{}按钮点击失败".format(description))
                return False
        except Exception as msg:
            self._logger.exception("{}锁定点击异常，异常信息：{}".format(description, msg))
            return False

    def find_element_by_xpath_with_send_keys(self, xpath, text, description="TEXT"):

        try:
            text_element = self.find_element_by_xpath(xpath, description)
            if text_element:
                time.sleep(0.5)
                text_element.send_keys(text)
                time.sleep(random.randint(2, 3))
                self._logger.info("{}内容填充完成".format(description))
                return True
            else:
                self._logger.error("{}内容填充失败".format(description))
                return False
        except Exception as msg:
            self._logger.exception("{}内容填充异常，异常信息：{}".format(description, msg))
            return False

    def __del__(self):

        pass
