#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 消息类型定义
class MsgType(object):
    """MsgType class are used to save socket communicate msg type info."""

    NONE = 0

    # SOCIAL_TASK_REQ = 0x00030001            # 社交任务请求
    # SOCIAL_TASK_REQ_ANS = 0x10030001   # 社交任务请求响应
    # ACCOUNT_STATE_REQ = 0x00030005       # 账号资源状态上报
    # ACCOUNT_STATE_REQ_ANS = 0x10030005   # 账号资源状态上报响应
    Heart_request = 0x00010000  # 心跳请求
    Heart_response = 0x10010000  # 心跳响应

    Account_Task_request = 0x00010001  # 账号登录验证请求 msgType
    Account_response = 0x10010001  # 账号登录验证响应 msgType

    Like_Task_request = 0x00010002  # 点赞任务请求 msgType
    Like_response = 0x10010002  # 点赞任务响应 msgType

    Tweet_Task_request = 0x00010003  # 发布推文任务请求 msgType
    Tweet_response = 0x10010003  # 发布推文任务响应 msgType

    Retweeted_Task_request = 0x00010004  # 转发推文任务请求 msgType
    Retweeted_response = 0x10010004  # 转发推文任务响应 msgType

    Comment_Task_request = 0x00010005  # 评论任务请求 msgType
    Comment_response = 0x10010005  # 评论任务响应 msgType

    Follow_Task_request = 0x00011000  # 关注任务请求 msgType
    Follow_response = 0x10011000  # 关注任务响应 msgType


# 消息头定义
class MsgInfoHead(object):
    """MsgInfoHead instances are used to record head info."""

    def __init__(self):
        self.msg_id = 0                # 消息ID
        self.msg_type = MsgType.NONE   # 消息类型
        self.msg_len = 0               # 消息总长度
        self.time_stamp = 0            # 时间戳


# 返回值集合
class RetCode(object):
    """MsgType class are used to record the return code of socket communication."""

    SUCCESS = 0        # 成功
    TIMEOUT_ERROR = 1  # 等待超时
    NETWORK_ERROR = 2  # 网络异常
    FORMAT_ERROR = 3   # 格式错误
    NO_RESOURCE = 4    # 无任务
    HAVE_RESOURCE = 5  # 有任务
    PARSE_ERROR = 6    # 解析错误
    BUILD_ERROR = 7    # 创建消息错误
    OTHER_ERROR = 8    # 其他错误
    STOP_COON = 9     # 断开连接


# Socket建链信息
class SocketServerInfo(object):
    """SocketServerInfo instances are used to record connection information of client."""

    connect = None
    address = ""


msg_task_request = {
    "data": {
        "number": 0,
        "follow_list": [],
        "like_list": [],
        "reply_list": [
            {
                "content": "Beautiful meal!",
                "homepage": "https://twitter.com/jian_waner/status/1258950118025224193"
            }
        ],
        "retweet_list": [],
        "tweets": []
    }
}

msg_task_response = {
    "result": 0
}

msg_status_response = {
    "valid_accounts": 0,
    "invalid_accounts": 1
}
