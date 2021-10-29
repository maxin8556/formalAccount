import re, sys, time, os
import logging
import random, json
import base64
import mimetypes
import requests
from Utils.JsonTool import JsonTool
from Utils.cryptotool import CryptoTool
from TwitterApi import basic_headers, user_agent_list
from core.accountlogin.accountlogin import AccountLogin



class ResponseCode:
    OK = 200
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NODATA = -1
    EXCEPTION = -2


class TwitterApiAccess:

    def __init__(self):

        self.media_id = None
        self.processing_info = None
        self.upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        self.byte_file = './bytes_file/'
        if not os.path.exists(self.byte_file):  # 判断文件夹是否存在
            os.makedirs(self.byte_file)  # 新建文件夹
        else:
            pass

        self._logger = logging.getLogger()
        self._session = requests.session()

    @staticmethod
    def get_valid_cookies(cookies):
        """
        提取有效cookies字段
        """
        def transfer_cookies(cookies):
            if not isinstance(cookies, list):
                return {}
            else:
                _cookies = {}
                try:
                    for _cookie in cookies:
                        _cookies[_cookie["name"]] = _cookie["value"]
                    return _cookies
                except Exception as e:
                    return ""

        laconic_cookies = transfer_cookies(cookies)
        if isinstance(laconic_cookies, dict) and "ct0" in laconic_cookies and "auth_token" in laconic_cookies:
            _cookies = {
                "ct0": laconic_cookies["ct0"],
                "auth_token": laconic_cookies["auth_token"]
            }
            return _cookies
        return None

    def set_cookies(self, cookies):
        """
        设置会话cookies
        """
        _cookies = self.get_valid_cookies(cookies)
        if not _cookies:
            self._logger.error("未提取到有效cookies")
            return None
        self._session.cookies = requests.utils.cookiejar_from_dict(_cookies)
        # self._logger.info("存在可用cookies:{}".format(_cookies))
        return _cookies

    def _post(self, url, data, cookie_path, **kwargs):

        logging.info("进入post请求")
        cookie = kwargs.get("cookies", None)
        description = kwargs.get("description", None)
        basic_headers['x-csrf-token'] = cookie["ct0"]
        _headers = basic_headers
        self._session.headers = _headers

        try:
            response = self._session.post(url,
                                          data=data,
                                          cookies=cookie,
                                          timeout=(100, 120))
            self._logger.info(u'cookie状态码为:{}, json为:{}'.format(response.status_code, response.json()))
            if not str(response.status_code).startswith("2"):
                if response.status_code in [401]:
                    self._logger.error(u'cookie已失效，删除cookie缓存')
                    # return response.status_code, 'cookie已失效，删除cookie缓存'
                    # return 3, '账号异常'
                    # 重新登录，获取cookie（获取到重新执行post请求，没有获取到网络异常）
                    account_info = JsonTool.read_json_file(cookie_path)
                    # 读取文件解密
                    # print(account_info)
                    # print(type(account_info))
                    # aes_encrypt = AESEncrypt(AES_KEY)
                    account_info = CryptoTool().decrypt(account_info)
                    account_info = str(account_info, 'utf-8')
                    account_info = JsonTool().str_to_dict(account_info)

                    application = 'Twitter'
                    account_acc = account_info['homepage'].rstrip('/').split('/')[-1]
                    account_pas = account_info['password']
                    account_pho = account_info['phone_number']
                    account_infos = {
                        "appli": application,
                        "name": account_acc,
                        "password": account_pas,
                        "account": account_pho,
                    }
                    # print(account_infos)
                    object_browser = AccountLogin()
                    # print(object_browser)
                    status, msg, next_cookie = object_browser.account_login_with_cookies_return_next(account_infos)
                    logging.info("状态码和信息为:{},{}".format(status, msg, next_cookie))

                    if status == 0 and next_cookie:
                        # 更新cookie文件
                        # orignal_data = JsonTool.read_json_file(cookie_path)
                        # orignal_data.update({"cookies": next_cookie})

                        account_info.update({"cookies": next_cookie})

                        # 加密写入文件
                        account_info = CryptoTool().encrypt_from_dict_data(account_info)
                        # print(account_info)
                        # print(type(account_info))
                        account_info = str(account_info, 'utf-8')
                        # print(account_info)
                        # print(type(account_info))
                        JsonTool.write_json_file(account_info, cookie_path)

                        self._logger.info("进行更新cookie，重新社交")
                        _cookies = self.set_cookies(next_cookie)
                        # print(_cookies)
                        self._post(url, data, cookie_path, description=description, cookies=_cookies)

                    else:
                        self._logger.error("账号重新登录错误，网络异常")
                        return 6, "网络异常"

                elif response.status_code in [403, 404]:
                    try:
                        code = response.json()['errors'][0]['code']
                        self._logger.error("账号操作状态码为{},类型为:{}".format(code, type(code)))
                        if code in [139, 187, 327]:
                            self._logger.error("账号操作异常信息为{}".format(response.json()))
                            return 0, '重复操作'
                        elif code in [96, 385, 144, 108]:
                            self._logger.error("账号操作异常信息为{}".format(response.json()))
                            return 9, '帖子不存在或失效'
                        elif code in [170, 324, 408, 186]:
                            self._logger.error("账号操作异常信息为{}".format(response.json()))
                            return 5, '输入异常'
                        # elif code in [187 , 327]:
                        #     self._logger.error("账号操作异常信息为{}".format(response.json()))
                        #     return 13, '重复操作'
                        elif code in [326, 64, 283, 226]:
                            self._logger.error("账号操作异常信息为{}".format(response.json()))
                            return 2, '账号封停'
                        else:
                            self._logger.error("账号操作异常信息为{}".format(response.json()))
                            return 4, '任务失败'

                    except Exception as e:
                        self._logger.error("账号已经锁定，需要解锁后才可以使用！异常信息为{},json为{}".format(e,response.json()))
                        return 4, '任务失败'

            self._logger.info(u"{}操作完成，响应：{}".format(kwargs.get("description", "post"), response.json()))
            return 0, response.json()

        except Exception as msg:
            self._logger.exception(u"{}操作异常，异常信息：{}".format(kwargs.get("description", "post"), msg))
            return 4, '任务失败'

    def _get(self, url, **kwargs):
        _headers = basic_headers
        _headers["User-Agent"] = random.choice(user_agent_list)
        _headers["x-csrf-token"] = kwargs["cookies"]["ct0"]
        self._session.headers = _headers
        try:
            response = self._session.get(url,
                                         params=kwargs.get("params", None),
                                         timeout=(30, 120))
            if 200 != response.status_code:
                if 401 == response.status_code:
                    self._logger.error('cookie已失效，删除cookie缓存')
                elif 403 == response.status_code:
                    self._logger.error("账号已经锁定，需要解锁后才可以使用！")
                return response.status_code, {}
            self._logger.info(u"{}操作完成，状态：{}，响应：{}".format(
                kwargs.get("description", "get"), response.status_code, response.json()))
            return response.status_code, response.json()
        except Exception as msg:
            self._logger.exception(u"{}操作异常，异常信息：{}".format(kwargs.get("description", "post"), msg))
            return ResponseCode.EXCEPTION, {}

    def api_search_tweets(self, query, count=15):
        """
        搜索推文
        """
        _url = "https://api.twitter.com/1.1/search/tweets.json"
        params = {
            "q": query,
            "count": count,
            "include_entities": "false"
        }
        return self._get(_url, params=params, description="推文搜索",
                         cookies=requests.utils.dict_from_cookiejar(self._session.cookies))

    @staticmethod
    def get_tweet_id(homepage):
        """
        提取推文地址的ID
        """
        try:
            regex = re.compile(r"(\d+)$")
            groups = regex.search(homepage.strip())
            return groups.group()
        except Exception as e:
            return ""

    def api_like(self, tweet_id, cookie_c, cookie_path):
        """
        点赞
        """
        try:
            tweet_id = tweet_id.strip().rstrip('/').split('/')[-1]
        except Exception as e:
            self._logger.error(u"点赞url{}异常".format(tweet_id))
            return 5, "url{}异常".format(tweet_id)

        if tweet_id:
            self._logger.info(u"点赞url是{}".format(tweet_id))

            _url = "https://api.twitter.com/1.1/favorites/create.json"
            data = {
                "id": tweet_id
            }
            return self._post(_url, data, cookie_path, description="点赞",
                              cookies=cookie_c)
        else:
            self._logger.error(u"点赞url{}异常".format(tweet_id))
            return 5, "url{}异常".format(tweet_id)

    def api_reply(self, reply_info, reply_url, cookie_c, cookie_path):
        """
        评论
        """
        try:
            reply_url = reply_url.strip().rstrip('/').split('/')[-1]
        except Exception as e:
            self._logger.error(u"评论url{}异常".format(reply_url))
            return 5, "url{}异常".format(reply_url)

        if reply_url and reply_info:

            _url = "https://api.twitter.com/1.1/statuses/update.json"
            data = {
                'status': reply_info,
                'in_reply_to_status_id': reply_url,
                'auto_populate_reply_metadata': 'true'
            }
            return self._post(_url, data, cookie_path, description="评论",
                              cookies=cookie_c)
        else:
            self._logger.error(u"评论url{}和content{}异常".format(reply_url, reply_info))
            return 5, "url{}和content{}异常".format(reply_url, reply_info)

    def api_retweet(self, retweet_info, retweet_url, cookie_c, cookie_path):
        """
        转发
        """
        if len(retweet_info) > 0 and len(retweet_url) > 0:
            media_ids = []
            _url = "https://api.twitter.com/1.1/statuses/update.json"
            data = {
                'status': retweet_info,
                'media_ids': ",".join(media_ids),
                'attachment_url': retweet_url
            }
            self._logger.info(u"转推带内容url:{},转推内容:{}".format(retweet_url, retweet_info))
            return self._post(_url, data, cookie_path, description="转发带内容",
                              cookies=cookie_c)

        elif len(retweet_info) == 0 and len(retweet_url) > 0:

            try:
                retweet_url = retweet_url.strip().rstrip('/').split('/')[-1]
            except Exception as e:
                self._logger.error(u"转推url{}异常".format(retweet_url))
                return 5, "url{}异常".format(retweet_url)

            _url = "https://api.twitter.com/1.1/statuses/retweet/{}.json".format(retweet_url)
            data = {
                "id": retweet_url
            }
            self._logger.info(u"转推url_id:{}".format(retweet_url))
            return self._post(_url, data, cookie_path, description="转推",
                                    cookies=cookie_c)
        else:
            self._logger.error(u"转推url{},转发内容{}异常".format(retweet_url, retweet_info))
            return 5, "url{}异常".format(retweet_url)

    def api_search_users(self, query, count=5):
        """
        搜索用户
        """
        _url = "https://api.twitter.com/1.1/users/search.json"
        params = {
            "q": query,
            "count": count,
            "include_entities": "false"
        }
        return self._get(_url, params=params, description="用户搜索",
                         cookies=requests.utils.dict_from_cookiejar(self._session.cookies))

    def api_follow(self, tweet_follow_id, cookie_c, cookie_path):

        try:
            tweet_follow_id = tweet_follow_id.strip().rstrip('/').split('/')[-1]
        except Exception as e:
            self._logger.error(u"关注主页url{}异常".format(tweet_follow_id))
            return 5, "url{}异常".format(tweet_follow_id)

        _url = "https://api.twitter.com/1.1/friendships/create.json"
        data = {
            "screen_name": tweet_follow_id,
            "follow": "true"
        }
        # return self._post(_url, data=data, description="关注",
        #                   cookies=requests.utils.dict_from_cookiejar(self._session.cookies))

        return self._post(_url, data, cookie_path, description="关注",
                          cookies=cookie_c)

    def api_follow_auto(self, count, cookie_c, cookie_path):

        status, msg = '', ''

        header = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "x-csrf-token": cookie_c['ct0'],
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session"
        }

        _url = "https://api.twitter.com/1.1/friendships/create.json"

        discov_url = 'https://twitter.com/i/api/2/people_discovery/modules_urt.json'
        # req = requests.get(discov_url, headers=header, cookies=cookie_c, proxies=self.proxies)
        req = requests.get(discov_url, headers=header, cookies=cookie_c)
        print(req.status_code)
        # print(type(req.status_code))
        # req = req.text
        # print(req)

        if req.status_code in [401, 403]:

            # code = req.json()['errors'][0]['code']
            self._logger.error("账号操作状态码为{},内容为:{}".format(req.status_code, req.json()))
            # if code in [353]:
            self._logger.error(u'cookie已失效，删除cookie缓存')
            # 重新登录，获取cookie（获取到重新执行post请求，没有获取到网络异常）
            account_info = JsonTool.read_json_file(cookie_path)
            # 读取文件解密
            # print(account_info)
            # print(type(account_info))
            # aes_encrypt = AESEncrypt(AES_KEY)
            account_info = CryptoTool().decrypt(account_info)
            account_info = str(account_info, 'utf-8')
            account_info = JsonTool().str_to_dict(account_info)

            application = 'Twitter'
            # account_acc = account_info['name']
            account_acc = account_info['homepage'].rstrip('/').split('/')[-1]
            account_pas = account_info['password']
            account_pho = account_info['phone_number']
            account_infos = {
                "appli": application,
                "name": account_acc,
                "password": account_pas,
                "account": account_pho,
            }
            # print(account_infos)
            object_browser = AccountLogin()
            # print(object_browser)
            status, msg, next_cookie = object_browser.account_login_with_cookies_return_next(account_infos)
            logging.info("状态码和信息为:{},{}".format(status, msg))

            if status == 0 and next_cookie:
                # 更新cookie文件
                # orignal_data = JsonTool.read_json_file(cookie_path)
                # orignal_data.update({"cookies": next_cookie})
                account_info.update({"cookies": next_cookie})

                # 加密写入文件
                account_info = CryptoTool().encrypt_from_dict_data(account_info)
                # print(account_info)
                # print(type(account_info))
                account_info = str(account_info, 'utf-8')
                # print(account_info)
                # print(type(account_info))
                JsonTool.write_json_file(account_info, cookie_path)

                # 新cookie文件重新社交
                self._logger.info("进行更新cookie，重新社交")
                _cookies = self.set_cookies(next_cookie)
                # print(_cookies)
                status, msg = self.api_follow_auto(count, _cookies, cookie_path)
                if status == 0:
                    logging.info("状态码和信息为:{},{}".format(status, msg))
                    return 0, '关注成功'
                else:
                    logging.error("状态码和信息为:{},{}".format(status, msg))
                    return 6, "网络异常"
                # self._post(url, data, cookie_path, description=description, cookies=_cookies)

            else:
                self._logger.error("账号重新登录错误，网络异常")
                return 6, "网络异常"

        elif req.status_code in [200]:
            req = req.text
            print(req)
            req = json.loads(req)['globalObjects']['users']
            print(req)
            print(len(req))
            print(type(req))

            name_list = []
            for key in req:
                dic_name = {}
                dic_name[key] = req[key]
                name_list.append(dic_name)

            print('*' * 20)
            print(count)
            print(type(count))
            # print('*'*20)
            # count = int(count)
            # print(count)
            # print(type(count))

            for name_dic in name_list[0:count]:
                time.sleep(random.randint(3,8))
                name_val = name_dic.get(tuple(name_dic.keys())[0])
                print(name_val['screen_name'])
                print(type(name_val['screen_name']))

                data = {
                    "screen_name": name_val['screen_name'],
                    "follow": "true"
                }

                # return self._post(_url, data, cookie_path, description="关注",
                #                   cookies=cookie_c)
                status, msg = self._post(_url, data, cookie_path, description="关注",
                                  cookies=cookie_c)
                print('='*20)
                print(status, msg)

            return status, msg
            # return 0, '关注成功'

        else:
            self._logger.error("账号操作状态码为{},类型为:{}".format(req.status_code, type(req.status_code)))
            return 6, "网络异常"

    def api_tweet(self, tweet_info, tweet_names, tweet_fileBytes, cookie_c, cookie_path):

        media_ids = []
        if len(tweet_names) > 0 and len(tweet_names) != len(tweet_fileBytes):
            self._logger.info("进入有名字缺少或没有数据流里面")
            for tweet_name in tweet_names:
                # 循环多媒体文件夹寻找有木有相同的文件名字
                for root, dirs, files in os.walk(self.byte_file):
                    for f in files:
                        if tweet_name == f:
                            data_file = open(f, 'rb')
                            data = data_file.read()
                            tweet_fileBytes.append(data)
                        else:
                            print("continue")
                            continue

            self._logger.info("推文文件名{}长度{},推文数据长度{}".format(tweet_names,len(tweet_names),len(tweet_fileBytes)))
            if len(tweet_names) == len(tweet_fileBytes):
                self._logger.info("服务器有该文件数据")
                media_ids = self.test_upload_media(tweet_names, tweet_fileBytes, cookie_c, cookie_path)
            else:
                self._logger.info("服务器没有该文件数据")
                return 5, "输入异常"

        elif len(tweet_names) > 0 and len(tweet_names) == len(tweet_fileBytes):
            self._logger.info("进入有名字也有数据流里面")
            media_ids = self.test_upload_media(tweet_names, tweet_fileBytes, cookie_c, cookie_path)

        else:
            media_ids = None

        if media_ids is None:
            media_ids = []

        _url = "https://api.twitter.com/1.1/statuses/update.json"
        data = {
            'status': tweet_info,
            'media_ids': ",".join(media_ids)
        }
        return self._post(_url, data, cookie_path, description="发推",
                          cookies=cookie_c)


    @staticmethod
    def parse_media_file(passed_media, async_upload=False):

        img_formats = ['image/jpeg',
                       'image/png',
                       'image/bmp',
                       'image/webp']
        long_img_formats = [
            'image/gif'
        ]
        video_formats = ['video/mp4',
                         'video/quicktime']

        if not hasattr(passed_media, 'read'):
            data_file = open(os.path.realpath(passed_media), 'rb')
            filename = os.path.basename(passed_media)

        # Otherwise, if a file object was passed in the first place,
        # create the standard reference to media_file (i.e., rename it to fp).
        else:
            if passed_media.mode not in ['rb', 'rb+', 'w+b']:
                raise Exception('File mode must be "rb" or "rb+"')
            filename = os.path.basename(passed_media.name)
            data_file = passed_media

        data_file.seek(0, 2)
        file_size = data_file.tell()
        media_type = mimetypes.guess_type(os.path.basename(filename))[0]

        if media_type is not None:
            if media_type in img_formats and file_size > 5 * 1048576:
                raise Exception({'message': 'Images must be less than 5MB.'})
            elif media_type in long_img_formats and file_size > 15 * 1048576:
                raise Exception({'message': 'GIF Image must be less than 15MB.'})
            elif media_type in video_formats and not async_upload and file_size > 15 * 1048576:
                raise Exception({'message': 'Videos must be less than 15MB.'})
            elif media_type in video_formats and async_upload and file_size > 512 * 1048576:
                raise Exception({'message': 'Videos must be less than 512MB.'})
            elif media_type not in img_formats and media_type not in video_formats and media_type not in long_img_formats:
                raise Exception({'message': 'Media type could not be determined.'})
        if media_type in img_formats:
            media_category = "tweet_image"
            return data_file, filename, file_size, media_type, media_category
        elif media_type in long_img_formats:
            media_category = "tweet_gif"
            return data_file, filename, file_size, media_type, media_category
        elif media_type in video_formats:
            media_category = "tweet_video"
            return data_file, filename, file_size, media_type, media_category

    # 发表带有多媒体的推文
    def test_upload_media(self, tweet_names, tweet_fileBytes, cookies, cookie_path):

        media_ids = []

        for tweet_name, tweet_fileByte in zip(tweet_names, tweet_fileBytes):
            # 二进制数据生成文件
            passed_media = self.byte_file + tweet_name
            # str类型的base64转换成bytes
            tweet_fileByte = base64.b64decode(tweet_fileByte)
            file = open(passed_media, 'wb')
            file.write(tweet_fileByte)
            file.close()
            try:
                media_data, media_name, media_size, media_type, media_category = self.parse_media_file(passed_media=passed_media)
                self._logger.info("media_name, media_size, media_type, media_category为{},{},{},{}".format(media_name, media_size, media_type, media_category))
                self.upload_init(media_size, media_type, media_category, cookies, cookie_path)
                self.upload_append(media_name, media_size, cookies)
                self.upload_finalize(cookies)
                media_ids.append(self.media_id)
            except Exception as e:
                self._logger.error("处理错误信息是{}".format(e))

        return media_ids

    def upload_init(self, media_size, media_type, media_category, cookies, cookie_path):
        '''
        Initializes Upload
        '''
        self._logger.info("INIT")
        init_data = {
            "command": "INIT",
            "total_bytes": media_size,
            "media_type": media_type,
            'media_category': media_category
        }

        # 获取多媒体id
        tweet_status, init_response = self._post(self.upload_url, init_data, cookie_path, cookies=cookies)
        self._logger.info("tweet_status, init_response为{},{}".format(tweet_status, init_response))
        self.media_id = init_response["media_id_string"]
        self._logger.info("多媒体ID:{}".format(self.media_id))

    def upload_append(self, media_name, media_size, cookies):
        '''
        Uploads media in chunks and appends to chunks uploaded
        '''
        self._logger.info('APPEND')
        segment_id = 0
        bytes_sent = 0
        media_name = self.byte_file + media_name
        self._logger.info('media_name是{}'.format(media_name))
        file = open(media_name, 'rb')

        while bytes_sent < media_size:
            base64_data = base64.b64encode(file.read(4 * 1024 * 1024))
            data = base64_data.decode()
            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id,
                'media': data
                # 'media_data': data
            }

            req = self._session.post(url=self.upload_url, data=request_data, cookies=cookies)
            self._logger.info('status_code,text是{},{}'.format(req.status_code,req.text))
            if req.status_code < 200 or req.status_code > 299:
                sys.exit(0)

            segment_id = segment_id + 1
            self._logger.info('segment_id是{}'.format(segment_id))
            bytes_sent = file.tell()
            self._logger.info("{} of {} bytes uploaded".format(str(bytes_sent), str(media_size)))

            self._logger.info('Upload chunks complete.')

    def upload_finalize(self, cookies):
        '''
        Finalizes uploads and starts video processing
        '''
        self._logger.info('FINALIZE')
        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        req = self._session.post(url=self.upload_url, data=request_data, cookies=cookies)
        self._logger.info("req.json是{}".format(req.json()))

        self.processing_info = req.json().get('processing_info', None)
        self._logger.info("processing_info是{}".format(self.processing_info))
        self.check_status(cookies)

    def check_status(self, cookies):
        '''
        Checks video processing status
        '''
        if self.processing_info is None:
            return

        state = self.processing_info['state']
        self._logger.info("Media processing status is {}".format(state))

        if state == u'succeeded':
            return

        if state == u'failed':
            sys.exit(0)

        check_after_secs = self.processing_info['check_after_secs']
        self._logger.info("Checking after {} seconds".format(str(check_after_secs)))
        time.sleep(check_after_secs)
        self._logger.info('STATUS')
        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }
        req = self._session.get(url=self.upload_url, params=request_params, cookies=cookies)
        self._logger.info("req.status_code,req.text是{},{}".format(req.status_code,req.text))
        self.processing_info = req.json().get('processing_info', None)
        self.check_status(cookies)
