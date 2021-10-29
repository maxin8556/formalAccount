#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
站点元素定位文件
"""


class HtcElement():
    cookie_is_on_element = {
        'xpath': '//*[@id="htc_nav_me"]'
    }
    login_is_on_element = {
        'xpath': '//*[@id="js-back-url"]'
    }

    username_element = {
        "xpath": '//*[@id="app"]/div[1]/div/div/form/div[2]/div[3]/div/div/div/input',
    }
    password_element = {
        "xpath": '//*[@id="app"]/div[1]/div/div/form/div[2]/div[4]/div/div/div[1]/div/input',
    }
    login_element = {
        'xpath': '//*[@id="app"]/div[1]/div/div/form/div[2]/div[6]/div/button'
    }

    htc_post = {
        'title_id': 'subject',
        'text_xpath': '//body',
        # 点击图片按钮
        'imageClick1_xpath': '//*[@id="e_image"]',
        # 选择图片发送
        'imageInput1_xpath': '//*[@id="imgattachnew_1"]',
        'imageInput2_xpath': '//*[@id="imgattachnew_2"]',
        # 点击上传按钮
        'imageClick2_xpath': '//*[@id="imguploadbtn"]/button',
        # 上传图片
        'imagePost1_xpath': '//div[@id="imgattachlist"]/table//td[1]',
        'imagePost2_xpath': '//div[@id="imgattachlist"]/table//td[2]',
        # 帖子发布
        'post_xpath': '//*[@id="postsubmit"]'
    }


class NybbsElement():
    is_on_element = {
        'class': 'has-login'
    }
    username_element = {
        "name": "username"
    }
    password_element = {
        "name": "password"
    }
    login_element = {
        'name': 'loginsubmit'
    }

    nybbs_post = {
        # 标题
        'title_name': 'subject',
        # 文本
        'text_xpath': '//body',
        # 图片发送
        # 先点击图片按钮,然后上传图片,再然后点击图片
        'image_click1_id': 'e_image',
        # 上传图片
        'imageInput_name': 'file',
        # 点击图片上传
        'imagePost1_xpath': '//table[@class="imgl"]//tr/td[1]',
        'imagePost2_xpath': '//table[@class="imgl"]//tr/td[2]',
        # 发送帖子
        'post_id': 'postsubmit',
    }


class UlifestyleElement():
    # 登录需要的账号密码,登录键的元素
    username_element = {
        "id": "username"
    }
    password_element = {
        "id": "password"
    }
    login_element = {
        'id': 'btn-submit'
    }

    is_on_element = {
        'class': 'profile-dropdown__profilePicWrapper'
    }

    # 发帖元素===
    ulifestyle_element = {
        # 标题
        "title_id": 'post-title',
        # 文本
        "text_xpath": '//*[@id="editor"]/div[1]',
        # 图片
        "image_id": 'upload-post-photo',
        # 发布帖子
        "post_xpath": '//*[@id="app"]/div[2]/div/div[2]/button',
        # 发布分类
        'classify_xpath': '//*[@id="app"]/div[3]/div/div[2]/div[3]/div/div[4]',
        # 点击发送
        'postClick_xpath': '//*[@id="app"]/div[4]/div[1]/div/div/button',

    }


class ShowweElement():
    # 登录需要的账号密码,登录键的元素
    username_element = {
        "id": "c1_TextBox1"
    }
    password_element = {
        "id": "c1_TextBox2"
    }
    login_element = {
        'id': 'c1_btnLogin'
    }

    is_on_element = {
        'id': 'Head1_limember'
    }

    # 发帖元素===
    showwe_element = {
        # 标题
        "title_name": 'ctl00$c1$txtTitle',
        # 文本
        "text_xpath": '//body',
        # 图片
        "image_name": 'ctl00$c1$FileUpload1',
        # 发布帖子
        "post_name": 'ctl00$c1$btnSend',

    }


class PixnetElement():
    # 登录需要的账号密码,登录键的元素
    username_element = {
        "name": "email"
    }
    password_element = {
        "name": "password"
    }
    login_element = {
        'xpath': '//*[@id="signin__form--post"]/button'
    }

    is_on_element = {
        'xpath': '//*[@id="root"]/div[1]/div[1]/a/span'
    }

    # 发帖元素===
    pixnet_element = {
        # 发帖按钮
        "goPost_xpath": '//*[@id="main"]/div[3]/div/div/div/div[1]/div',
        # 标题
        "title_id": 'myEditor',
        # 文本
        "text_id": 'myEditor',
        # 图片
        "image_xpath": '//*[@id="vue-root"]/div[4]/div/footer/div/ul/li/input',
        # 发布帖子
        "post_xpath": '//*[@id="vue-root"]/div[4]/div/footer/div/button',

    }


class TumblrElement():
    # 登录需要的账号密码,登录键的元素
    username_element = {
        "name": "email"
    }
    password_element = {
        "name": "password"
    }
    login_element = {
        "class": "vq1BT"
    }

    # 判断是否登录的元素
    is_on_element = {
        'class': 'WxJdZ.BPAd0'
    }

    # 发帖元素===
    tumblr_element = {
        # 标题
        "title": '//*[@id="redpop_iframePostForms"]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]',
        # 文本
        "text": '//*[@id="redpop_iframePostForms"]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]',
        # 图片
        "image": '//*[@id="redpop_iframePostForms"]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[5]/div[2]/div[1]/input',
        # 发布帖子
        "post": '//*[@id="redpop_iframePostForms"]/div[3]/div/div/div/div/div[2]/div[2]/div/div[5]/div[1]/div/div[3]/div/div/button',

    }


class RedditElement():
    # 登录需要的账号密码,登录键的元素
    username_element = {
        "id": "loginUsername"
    }
    password_element = {
        "id": "loginPassword"
    }
    login_element = {
        "class": "AnimatedForm__submitButton.m-full-width"
    }

    is_on_element = {
        'class': '_3uVYL9qgX3QSEa_F4F-DPv.icon.icon-add'
    }

    # 发帖元素===
    reddit_element = {
        # 社区选择
        "Community": '//div[@class="anPJr_ybRailY8NbAunl2"]/input',
        # 标题
        "title": '//div[@class="_2wyvfFW3oNcCs5GVkmcJ8z"]/textarea',
        # 文本
        "text": '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/div[3]/div/div[1]/div/div/div',
        # 图片
        "image": '//div[@class="_3oLr47tuKGv2mNpavCZ2X0"]/span[16]/button/input',
        # "image_xpath":'//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/div[1]/div[1]/div/span[16]/button/div',
        # 发布帖子
        "post": '//div[@class="_2DHDj0dbS1TkKD3fMqSbHy"]/div/div[1]/button',

    }


class BloggerElement():
    is_on_element = {
        'class': 'MIJMVe'
    }
    # 登录需要的账号密码,登录键的元素
    blogger_login = {
        # 邮箱名称
        'username_name': 'identifier',
        # 下一步按钮
        'next_class': 'VfPpkd-vQzf8d',
        # VfPpkd-vQzf8d
        # 密码
        'password_name': 'password',
        # 登录
        'Longin_class': 'VfPpkd-vQzf8d'
    }

    blogger_post_element = {
        # 发帖按钮
        'go_post_class': 'MIJMVe',
        'title_class': 'whsOnd.zHQkBf',
        # 图片点击按钮
        'imageClick_class': 'DPvwYc.sm8sCf.GHpiyd',
        # 'imageClick_xpath':'//*[@id="ow556"]/span/span/span',
        # 'imageClick_xpath2':'//div[@class="JPdR6b e5Emjc qjTEB"]/div/div/span[1]/div[3]/div',
        'imageClick_xpath2': '//*[@id="yDmH0d"]/c-wiz[2]/div/c-wiz/div/div[2]/div/div/div[3]/span/div/div[1]/div[1]/div[1]/div[24]/div/div/span[1]',
        # 'imageClick_xpath3': '//div[@class="ge-Tl"]/input',
        'imageClick_xpath3': '//*[@id="doclist"]/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[1]/input',
        'image_xpath': '//*[@id="picker:ap:0"]',

        'text_xpath': '//body',
        # 'text_class': 'separator',
        'post_xpath': '//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div/div[1]/div[2]/div[4]/span/span/div',

        # 确定发布
        'definePost_xpath': '//*[@id="yDmH0d"]/div[4]/div/div[2]/div[3]/div[2]/span/span'
    }


class MattersElement():
    # 判断是否登录
    is_on_element = {
        'xpath': '//*[@id="__next"]/div/main/nav/section/ul/li[4]/button'
    }
    # 登录需要的账号密码,登录键的元素
    matters_login = {
        # 登录按钮
        'goLogin_xpath': '//*[@id="__next"]/div/main/article/header/section/section/section/button[1]/div/span/span',
        # 邮箱名称
        'username_xpath': '//*[@id="field-email"]',
        # 密码
        'password_xpath': '//*[@id="field-password"]',
        # 登录
        'Longin_xpath': '/html/body/reach-portal/div[3]/div/div/div[2]/div/div/header/section[2]/button/div/span/span'
    }

    matters_post_element = {
        # 发帖元素
        'goPost_xpath': '//*[@id="__next"]/div/main/nav/section/ul/li[5]/button',

        # 标题
        'title_xpath': '//*[@id="__next"]/div/main/article/section/div/header/input',

        # 正文
        'text_xpath': '//*[@id="editor-article-container"]/div/div/div[1]',

        # 点击工具栏出现发布图片选项
        'image_click1_xpath': '//*[@id="editor-article-container"]/aside/button',
        # 上传图片
        'image_xpath': '//*[@id="editor-article-container"]/aside/div/label[1]/input',

        # 发布
        'post_xpath': '//*[@id="__next"]/div/main/article/header/section/section[2]/button',

        # 确认发布
        'confirmPost_xpath': '/html/body/reach-portal/div[3]/div/div/div[2]/div/div/section/ul/footer/button[1]',

        # 再次确认发布
        'againConfirm_xpath': '/html/body/reach-portal/div[3]/div/div/div[2]/div/div/header/section[2]/button',

        # 点击查看作品
        'see_click': '/html/body/reach-portal/div[3]/div/div/div[2]/div/div/footer/button'

    }


class YorkbbsElement():
    username_element = {
        "id": "username"
    }
    password_element = {
        "id": "password"
    }
    login_element = {
        "class": "RButton.f16"
    }

    is_on_element = {
        'id': 'icon_pm'
    }

    activity_xpath = {
        "account_xpath": '//div[@class="Bjq_name f12 fl fontColorOne"]',
        "text_title_xpath": 'title',
        "text_content_xpath": 'wysiwyg',
        "button_iframe_xpath": 'posteditor_iframe',
        "button_iframe_media_xpath": 'posteditor_upload_iframe',
        "button_post_xpath": 'postsubmit',
        "click_pic": 'posteditor_popup_image',
        "click_pic_next": 'posteditor_btn_upload',
        "post_pic": 'postfile'
    }


class SkyscraperElement():
    is_on_element = {
        'xpath': '//*[@id="header"]/div/div/div[3]/span'
    }

    skyscraper_login = {
        # 登录按钮
        'goLogin_xpath': '//*[@id="header"]/div/div/div[3]/a[3]/span',
        # 邮箱名称
        'username_name': 'login',
        # 密码
        'password_name': 'password',
        # 登录
        'Longin_xpath': '//*[@id="js-XFUniqueId10"]/div/div[2]/div/div[3]/div[1]/form/div/div[4]/button'
    }

    skyscraper_post = {
        # 标题
        'title_name': 'title',
        # 文本
        'text_xpath': '//*[@id="create-thread-form"]/div/div[1]/div[2]/dl[1]/dd/div[1]/div[1]/div',
        # 图片点击
        'image_xpath_click': '//*[@id="insertImage-1"]',
        # 图片发送
        'go_image_xpath': '//*[@id="fr-image-upload-layer-1"]/div/input',
        # 发送帖子
        'post_xpath': '//*[@id="create-thread-form"]/div/div[4]/dd/div/div/button[1]',
    }


class KomicaElement():
    is_on_element = {
        'id': 'Komica'
    }

    Komica_post = {
        # 名称
        'name_id': 'fname',
        # email
        'password_id': 'femail',
        # 标题
        'title_id': 'fsub',
        # 文本
        'text_xpath': '//*[@id="fcom"]',
        # 图片发送
        'image_xpath': '//*[@id="postform_tbl"]/tbody/tr[5]/td[2]/input[1]',
        # 发送帖子
        'post_name': 'sendbtn',
    }
