#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 7/28/21 10:29 AM
# @Author: kevin
# @File: setting.py
# @Software: PyCharm


# 文件配置定义
class FileType(object):
    # content_path = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-forumSpider/AccountForum_Linux" \
    #                     "/loginData/content.json"
    # login_path = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-forumSpider/AccountForum_Linux" \
    #                   "/loginData/loginUrl.json"
    content_path = "./loginData/content.json"
    login_path = "./loginData/loginUrl.json"
    byte_file = "./bytes_file/"

    cookieYorkbbsPath = "/root/mx/AccountForum/cookieData/cookieyorkbbs"
    cookieTumblrPath = '/root/mx/AccountForum/cookieData/cookietumblr'
    cookieRedditPath = '/root/mx/AccountForum/cookieData/cookiereddit'
    cookieBloggerPath = '/root/mx/AccountForum/cookieData/cookieblogger'
    cookieMattersPath = '/root/mx/AccountForum/cookieData/cookiematters'
    # 这个网址不需要登录,直接不获取cookie了
    cookieKomicaPath = ''
    cookiePixnetPath = '/root/mx/AccountForum/cookieData/cookiepixnet'
    cookieShowwePath = '/root/mx/AccountForum/cookieData/cookieshowwe'
    cookieUlifestylePath = '/root/mx/AccountForum/cookieData/cookieulifestyle'
    cookieNybbsPath = '/root/mx/AccountForum/cookieData/cookienybbs'
    cookieHtcPath = '/root/mx/AccountForum/cookieData/cookiehtc'

    # cookie_path = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-forumSpider/AccountForum_Linux/cookieData/cookieYkbbs"

    # # 申请账号文件目录
    # apply_tw_dir = "/home/files/tw/apply_data/"
    # apply_fb_dir = "/home/files/fb/apply_data/"
    # # 申请账号文件名字
    # apply_name = "apply_data"
    # # 登录成功文件目录
    # login_tw_dir = "/home/files/tw/login_data/"
    # login_fb_dir = "/home/files/fb/login_data/"
    # # 登录成功文件名字
    # login_name = "login_data"
    # # 异常状态文件目录
    # normal_tw_dir = "/home/files/tw/normal_data/"
    # normal_fb_dir = "/home/files/fb/normal_data/"
    # # 异常状态文件名字
    # normal_name = "normal_data"
    # # 文件目录
    # file_dir = "/home/files/html/"
    # # 多媒体目录
    # media_dir = "/home/files/media/"
    # # 临时存放目录
    # tmp_dir = "/home/files/tmp/"
    # # tw本地存储cookie目录
    # tw_cookie_dir = "/home/cookie_tw"
    # # tw本地存储成功和失败总cookie目录
    # tw_allCookie_dir = "/home/cookie_allTw"
    # # fb本地存储cookie目录
    # fb_cookie_dir = "/home/cookie_fb"
    # # fb本地存储成功和失败cookie目录
    # fb_allCookie_dir = "/home/cookie_allFb"
    # # twitter应用名
    # appTwId = "Twitter"
    # # facebook应用名
    # appFbId = "Facebook"
    # # weibo应用名
    # appWbId = "Weibo"
    # # youtube应用名
    # appYtId = "YouTube"
    # # 区域编码
    # regionCode = "00081"
    # ip地址
    # 测试环境
    # ip = "167.179.110.186"

    # 演示环境
    # =======
    ip = "185.243.41.252"

    # 端口
    port = 20250
    # # 压缩包密码
    # zip_password = "elex123"
    # # 有异常标志
    # exceptionFlagTrue = "true"
    # # 无异常标志
    # exceptionFlagFalse = "false"

    # # 申请账号文件目录
    # apply_tw_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/tw/apply_data/"
    # apply_fb_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/fb/apply_data/"
    # # 申请账号文件名字
    # apply_name = "apply_data"
    # # 登录成功文件目录
    # login_tw_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/tw/login_data/"
    # login_fb_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/fb/login_data/"
    # # 登录成功文件名字
    # login_name = "login_data"
    # # 异常状态文件目录
    # normal_tw_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/tw/normal_data/"
    # normal_fb_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/fb/normal_data/"
    # # 异常状态文件名字
    # normal_name = "normal_data"
    # # 文件目录
    # file_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/html/"
    # # 多媒体目录
    # media_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/media/"
    # # 临时存放目录
    # tmp_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/files/tmp/"
    # # tw本地存储cookie目录
    # tw_cookie_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/cookie_tw"
    # # tw本地存储成功和失败总cookie目录
    # tw_allCookie_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/cookie_allTw"
    # # fb本地存储cookie目录
    # fb_cookie_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/cookie_fb"
    # # fb本地存储成功和失败cookie目录
    # fb_allCookie_dir = "/Users/xuxin/Desktop/upLinux/博智代码整理/yq-twSpider/Twitter_spider/cookie_allFb"
    # # twitter应用名
    # appTwId = "Twitter"
    # # facebook应用名
    # appFbId = "Facebook"
    # # weibo应用名
    # appWbId = "Weibo"
    # # youtube应用名
    # appYtId = "YouTube"
    # # 区域编码
    # regionCode = "00081"
    # # ip地址
    # ip = "103.56.19.10"
    # # 端口
    # port = 20277
    # # 压缩包密码
    # zip_password = "elex123"
    # # 有异常标志
    # exceptionFlagTrue = "true"
    # # 无异常标志
    # exceptionFlagFalse = "false"


# 应用类型
class AppType(object):
    twApp = "TW"
    fbApp = "FB"
    wbApp = "WB"
    ytApp = "YT"
    yorkbbs_user = "yorkbbs"
    reddit_user = "reddit"
    tumblr_user = "tumblr"
    blogger_user = "blogger"
    matters_user = "matters"
    komica_user = "komica"
    pixnet_user = "pixnet"
    showwe_user = "showwe"
    ulifestyle_user = "ulifestyle"
    nybbs_user = "nybbs"
    htc_user = "htc"


# 各类接口文件类型
class AppFileType(object):
    # 账号信息
    accInformation = "001"
    # 账号头像
    accProImage = "002"
    # 账号好友关系
    accRelation = "003"
    # 帖子动态
    accPost = "004"
    # 帖子图片
    accPicture = "005"
    # 帖子视频
    accVideo = "006"
    # 趋势采集
    accTrend = "007"
    # 小组信息
    groupInformation = "008"
    # 小组头像
    groupProImage = "009"
    # 小组帖子动态
    groupPost = "010"
    # 小组帖子图片
    groupPicture = "011"
    # 小组帖子视频
    groupVideo = "012"


user_agent = [
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 ',
    '(KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/31.0.1650.16 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
]




