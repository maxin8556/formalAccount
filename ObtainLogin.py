import re
import os
import logging
from Utils.utils import get_absolute_path
from core.accountlogin.accountlogin import AccountLogin
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton
LoggerSingleton().init_dict_config(LOGGING_CONFIG)


# 检查cookie存在否
def check_acc(account_acc):

    print(account_acc)
    cookie_files = get_absolute_path("./result")
    list = os.listdir(cookie_files)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(cookie_files, list[i])
        print(path)
        file_name = path.split("/")[-1].split("-")[1]
        print(file_name)

        if account_acc == file_name:
            logging.info("登陆账号已存在：{}".format(account_acc))

            return True

        else:

            print("登陆----------")
            continue

    return False


def login_begin(application, account_pho, account_pas, account_acc):

    account_info = ""

    if check_acc(account_acc) is True:

        return 0, ""

    else:
        if application and account_pas and account_acc:
            account_info = {
                "appli": application,
                "name": account_acc,
                "password": account_pas,
                "account": account_pho,
            }
            # logging.info("登陆账号：{}".format(account_info))
        else:
            # logging.info("传入参数异常为：{},{},{},{}".format(application, account_pho, account_pas, account_acc))
            return 5, "输入异常"

        object_browser = AccountLogin()
        status, msg = object_browser.account_login_with_cookies_return(account_info)
        logging.info("状态码和信息为:{},{}".format(status, msg))
        # return status, msg

        if 0 == status:
            return 0, "操作已成功"
        elif 1 == status:
            return 1, "账号不存在"
        elif 2 == status:
            return 2, "账号封停"
        elif 3 == status:
            return 3, "登录失效"
        elif 4 == status:
            return 4, "账号操作异常"
        elif 5 == status:
            return 5, "输入异常"
        elif 6 == status:
            return 6, "网络异常"
        elif 7 == status:
            return 7, "用户名或密码错误"
        elif 9 == status:
            return 9, "帖子不存在或失效"
        elif 12 == status:
            return 12, "无效链接"
        elif 13 == status:
            return 13, "重复操作"
        else:
            return 1, "账号不存在"
