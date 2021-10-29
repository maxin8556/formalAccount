#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 7/12/21 4:54 PM
# @Author: kevin
# @File: FBInfoDef.py
# @Software: PyCharm

from enum import Enum


class FBRetCode(Enum):
    """FriendRetCode class are used to save the state of friend homepage url."""
    SUCCESS = 0           # 成功
    LINK_OVERDUE = 1      # 过期
    ACCOUNT_DISABLED = 2  # 禁用
    PARSE_FAILED = 3      # 解析失败
    OTHER_ERROR = 4       # 其他原因
    REPEAT_FAILD = 5       # 重复发帖
