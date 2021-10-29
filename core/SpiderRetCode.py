#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 7/12/21 4:54 PM
# @Author: kevin
# @File: FBInfoDef.py
# @Software: PyCharm

from enum import Enum


# 浏览器状态
class BrowserState(Enum):
    """Browser state code."""
    TYPE_ONLINE = 0     # 账号在线
    TYPE_OFFLINE = 1    # 账号离线
    TYPE_INVALID = 2    # 账号无效
    TYPE_OTHERS = 3     # 未知原因
    TYPE_EXCEPTION = 4  # 浏览器异常


# 账号登陆状态
class AccountLoginStatus(Enum):
    """Account login status."""
    NORMAL = 0
    PASSWORD_ERROR = 1
    ACCOUNT_ERROR = 2
    SECURITY_ERROR = 3
    DISABLED_ERROR = 4
    UNKNOWN_ERROR = 5


class SelenRetCode(Enum):
    """Browser selenium operate return code."""
    SUCCESS = 0
    FORMAT_ERROR = 1
    BROWSER_ERROR = 2


class RetCode(Enum):
    """Homepage url open operate return code."""
    SUCCESS = 0
    BROWSER_ERROR = 1
    ACCOUNT_INVALID = 2
    LINK_INVALID = 3
    OTHER_ERROR = 4
    REPEAT_FAILED = 5
