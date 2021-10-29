import os
import time
import random
import datetime
from core.browserdriver.webdriver import WebService
from Utils.JsonTool import JsonTool
from Utils.utils import get_absolute_path
from Utils.cryptotool import CryptoTool


class AccountLogin(WebService):

    def __init__(self):
        super().__init__()

        self.save_path = get_absolute_path("./result")
        if not os.path.exists(self.save_path):
            os .makedirs(self.save_path)

    def twitter_login(self, account_info, **kwargs):

        if not self.open_browser():
            self._logger.info("进入self.open_browser")
            return None, 6, "浏览器打开异常"

        if "https://twitter.com/login" not in self._driver.current_url:

            self._logger.info("self._driver.get")
            self._logger.info(u"Twitter页面尚未打开，重新打开页面")
            self._driver.get("https://twitter.com/login")

        else:
            return None, 6, "浏览器首页打开异常"

        try:

            self._logger.info("进入try.......")
            self.clear_cookies()
            if not self.find_element_by_xpath_with_send_keys(kwargs["account_xpath"],
                                                             account_info["name"],
                                                             description="账号"):
                return None, 6, "账号填充异常"

            if not self.find_element_by_xpath_with_send_keys(kwargs["password_xpath"],
                                                             account_info["password"],
                                                             description="密码"):
                return None, 6, "密码填充异常"

            if not self.find_element_by_xpath_with_click(kwargs["login_xpath"], description="注册"):
                return None, 6, "注册点击异常"

            time.sleep(random.randint(2, 3))
            if self._driver.current_url == 'https://twitter.com/home':

                self._logger.info(u'账号登录模拟操作完成，用户=【{}】'.format(account_info.get("name")))
                return self._driver.get_cookies(), 0, ""

            err_content = self._driver.find_elements_by_xpath('//*[@id="react-root"]//main/div/div/div[1]/span')
            # self._logger.info('err_content：{}'.format(err_content))
            self._logger.info("--------------------------------")
            if not err_content:
                self._logger.info("===not err_content=====")
                err_content = self._driver.find_elements_by_class_name('PageContainer')

            err_str = ""
            for err in err_content:
                err_str = "".join(err.text)
                self._logger.info("----------err---------")
                self._logger.error(u'登陆失败，异常信息：{}'.format(err_str))
            self._logger.error(u'登陆失败，异常url：{}'.format(self._driver.current_url))

            # print(self._driver.current_url)
            self._logger.info("请求url为:{},type:{}".format((self._driver.current_url),type(self._driver.current_url)))
            if 'https://twitter.com/login/error?username_or_email' in self._driver.current_url:
                # if "The username and password you entered did not match our records. Please double-check and try again" in err_str:
                self._logger.info(u'账号登录失败login/error，用户=【{}】'.format(account_info.get("name")))
                return None, 7, "账号登录失败，{}账号密码错误再进行确认".format(account_info.get("name"))

            if 'https://twitter.com/login/check' in self._driver.current_url:
                self._logger.info(u'账号登录失败login/check，用户=【{}】'.format(account_info.get("name")))
                return None, 1, "账号登录失败，不存在该账号{}".format(account_info.get("name"))

            # 登陆失败异常检测--验证手机号--在有手机号码情况下
            if account_info["account"]:
                self._logger.info("----------进入手机验证---------")

                if "Report" in err_str:
                    self._logger.info("简单验证开始")
                    return self.verify_phone(account_info["account"].replace("+", "").strip())

                elif "Start" in err_str:
                    self._logger.info("复杂验证开始pass")
                    return None, 2, "需要人工验证"

                else:
                    return None, 2, err_str
            else:
                return None, 5, "账号登录失败，该账号不存在手机号码{}".format(account_info.get("name"))

        except Exception as msg:
            self._logger.exception(u"账号登录模拟操作异常，异常信息：{}".format(msg))
            return None, 2, msg

        finally:

            time.sleep(random.randint(2, 3))
            self.close_browser()

    def account_login_with_cookies_return(self, account_info):

        xpath_args = {
            "account_xpath": '//form[@action="/sessions" and @method="post"]'
                             '//input[@name="session[username_or_email]"]',
            "password_xpath": '//form[@action="/sessions" and @method="post"]'
                              '//input[@name="session[password]"]',
            "login_xpath": '//form[@action="/sessions" and @method="post"]/div/div[3]/div'
        }
        cookies, status, msg = self.twitter_login(account_info, **xpath_args)

        home_p = "https://twitter.com/" + account_info["name"]
        if 0 == status and cookies:
            # self._logger.info("进入status:{}和cookies:{}".format(status, cookies))
            self._logger.info("进入status:{}".format(status))

            record = {
                "actives": [],
                "activity_params": {
                    "type": "travel"
                },
                "cookies": cookies,
                "enable": True,
                "homepage": home_p,
                "name": account_info["name"],
                "password": account_info["password"],
                "phone_number": account_info["account"],
                "update_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # 加密
            file_name = "account-" + account_info["name"] + "-" + \
                        datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".json"
            aes_encrypt = CryptoTool().encrypt_from_dict_data(record)
            # print(aes_encrypt)
            # print(type(aes_encrypt))
            aes_encrypt_str = str(aes_encrypt, 'utf-8')
            # print(aes_encrypt_str)
            # print(type(aes_encrypt_str))
            JsonTool.write_json_file(aes_encrypt_str, file_name, self.save_path)

            # JsonTool.write_json_file(record,
            #                          file_name,
            #                          self.save_path)

            return 0, ""
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

        else:

            self._logger.error("没有有效cookie，状态码为{}".format(status))
            return 1, "账号不存在"

    def verify_phone(self, phone):

        verify_xpath = {
            "text_phone_xpath": '//div[@class="Section"]/form[@action="/account/login_challenge" and @id="login-challenge-form"]/input[@type="text" and @id="challenge_response"]',
            "button_submit_xpath": '//div[@class="Section"]/form[@action="/account/login_challenge" and @id="login-challenge-form"]/input[@type="submit" and @id="email_challenge_submit"]'
        }
        self._logger.info(u'验证手机')
        if not self.find_element_by_xpath_with_send_keys(verify_xpath["text_phone_xpath"],
                                                         phone,
                                                         description="手机"):
            return None, 6, "填充手机号码异常"
        self._logger.info("手机填充完成")

        if not self.find_element_by_xpath_with_click(verify_xpath["button_submit_xpath"],
                                                     description="提交"):
            return None, 6, "提交手机号码异常"
        self._logger.info("提交填充完成")

        time.sleep(random.randint(1, 2))
        if self._driver.current_url == 'https://twitter.com/home':

            self._logger.info(u'验证成功')
            return self._driver.get_cookies(), 0, ""

        else:

            self.record_web_status("验证失败结果")
            return None, 6, "验证手机失败"

    def account_login_with_cookies_return_next(self, account_info):

        xpath_args = {
            "account_xpath": '//form[@action="/sessions" and @method="post"]'
                             '//input[@name="session[username_or_email]"]',
            "password_xpath": '//form[@action="/sessions" and @method="post"]'
                              '//input[@name="session[password]"]',
            "login_xpath": '//form[@action="/sessions" and @method="post"]/div/div[3]/div'
        }
        cookies, status, msg = self.twitter_login(account_info, **xpath_args)

        if 0 == status and cookies:
            self._logger.info("有有效cookie，状态码为{}".format(status))
            return 0, "", cookies
        elif 2 == status:
            return 2, "账号封停", None
        elif 3 == status:
            return 3, "登录失效", None
        elif 5 == status:
            return 5, "输入异常", None
        elif 6 == status:
            return 6, "网络异常", None
        elif 7 == status:
            return 7, "用户名或密码错误", None
        else:
            self._logger.error("没有有效cookie，状态码为{}".format(status))
            return 1, "账号不存在", None
