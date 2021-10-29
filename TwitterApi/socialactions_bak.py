import random
import os, time
import datetime
import logging
import glob
from Utils.JsonTool import JsonTool
from TwitterApi.twitterapi import TwitterApiAccess, ResponseCode
from Utils.utils import get_absolute_path


class TaskType:
    TASK_LIKE = 1
    TASK_REPLY = 2
    TASK_RETWEET = 3
    TASK_TWEET = 4
    TASK_FOLLOW_APPOINT = 5
    TASK_FOLLOW_AUTO = 6
    # TASK_FOLLOW = 5


class AccountsAccess:

    def __init__(self):

        self._cache_breed_account = get_absolute_path("./data")
        self._cache_breed_account_backup = get_absolute_path("./data/accounts_backup")
        if not os.path.isdir(self._cache_breed_account_backup):
            os.makedirs(self._cache_breed_account_backup)

    def add_behavior_track(self, account_file, behavior):
        account_info = JsonTool.read_json_file(account_file)
        account_info["actives"].append(behavior)
        account_info["update_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        JsonTool.write_json_file(account_info, os.path.basename(account_file), os.path.dirname(account_file))

    def forbidden_account(self, file_path):
        orignal_data = JsonTool.read_json_file(file_path)
        orignal_data.update({"enable": False})
        JsonTool.write_json_file(orignal_data, file_path)


class CustomSocialActions(TwitterApiAccess):

    def tweet_with_like(self, path, account_info):

        cookies = {}

        _account_access = AccountsAccess()

        task_info = {
            "task_type": TaskType.TASK_LIKE,
            "task_status": None,
            "task_info": account_info['url'],
            "execute_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        account_info = JsonTool.read_json_file(path)

        if isinstance(account_info, dict) and "cookies" in account_info:
            for _cookie in account_info['cookies']:
                if _cookie["name"] in ["ct0", "auth_token"]:
                    cookies[_cookie["name"]] = _cookie["value"]

        task = {
            "task_file": path,
            "task_info": task_info,
            "cookies": account_info["cookies"],
            "account_type": account_info["activity_params"]["type"]
        }

        process_object = None

        def check_status(response_status, task_file_path):

            if response_status == ResponseCode.FORBIDDEN:
                _account_access.forbidden_account(task_file_path)
                logging.info("账号已锁定，禁用账号文件：{}".format(task_file_path))

        if not process_object:
            logging.info("进入process_object")
            process_object = CustomSocialActions()
            if not process_object.set_cookies(task["cookies"]):
                _account_access.forbidden_account(task["task_file"])
                logging.info("账号Cookies不可用，禁用账号文件：{}".format(task["task_file"]))
                # return ResponseCode.EXCEPTION, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])
                return 2, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])

        try:

            task["task_info"]["execute_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if task["task_info"]["task_type"] == TaskType.TASK_LIKE:

                like_status, like_response = self.api_like(
                    task["task_info"]["task_info"], cookies, path
                )
                task["task_info"]["task_status"] = like_status
                _account_access.add_behavior_track(task["task_file"], task["task_info"])
                check_status(like_status, task["task_file"])
                logging.info("处理任务类型：{}，处理结果：{}".format(task["task_info"]["task_type"], task["task_info"]))
                return like_status, like_response

            else:

                logging.error("未知任务类型：{}".format(task["task_info"]["task_type"]))
                return ResponseCode.EXCEPTION, "未知任务类型：{}".format(task["task_info"]["task_type"])
        except Exception as msg:

            logging.exception("任务:{}，处理异常，异常信息：{}".format(task, msg))
            return ResponseCode.EXCEPTION, msg
        finally:

            time.sleep(random.randint(1, 2))


    def tweet_with_tweet(self, path, account_infos):

        cookies = {}

        _account_access = AccountsAccess()

        task_info = {
            "task_type": TaskType.TASK_TWEET,
            "task_status": None,
            "task_info": account_infos['content'],
            "task_names": account_infos['names'],
            "execute_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        account_info = JsonTool.read_json_file(path)

        if isinstance(account_info, dict) and "cookies" in account_info:
            cookies = {}
            for _cookie in account_info['cookies']:
                if _cookie["name"] in ["ct0", "auth_token"]:
                    cookies[_cookie["name"]] = _cookie["value"]

        task = {
            "task_file": path,
            "task_info": task_info,
            "cookies": account_info['cookies'],
            "account_type": account_info["activity_params"]["type"]
        }

        process_object = None

        def check_status(response_status, task_file_path):

            if response_status == ResponseCode.FORBIDDEN:
                _account_access.forbidden_account(task_file_path)
                logging.info("账号已锁定，禁用账号文件：{}".format(task_file_path))

        if not process_object:
            logging.info("进入process_object")
            process_object = CustomSocialActions()
            if not process_object.set_cookies(task["cookies"]):
                _account_access.forbidden_account(task["task_file"])
                logging.info("账号Cookies不可用，禁用账号文件：{}".format(task["task_file"]))
                return 2, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])

        try:

            task["task_info"]["execute_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if task["task_info"]["task_type"] == TaskType.TASK_TWEET:
                tweet_status, tweet_response = self.api_tweet(
                    task["task_info"]["task_info"], task["task_info"]["task_names"],
                    account_infos['fileBytes'], cookies, path)

                task["task_info"]["task_status"] = tweet_status
                _account_access.add_behavior_track(task["task_file"], task["task_info"])
                check_status(tweet_status, task["task_file"])
                logging.info("处理任务类型：{}，处理结果：{}".format(task["task_info"]["task_type"], task["task_info"]))
                return tweet_status, tweet_response

            else:

                logging.error("未知任务类型：{}".format(task["task_info"]["task_type"]))
                return ResponseCode.EXCEPTION, "未知任务类型：{}".format(task["task_info"]["task_type"])
        except Exception as msg:

            logging.exception("任务:{}，处理异常，异常信息：{}".format(task, msg))
            return ResponseCode.EXCEPTION, msg
        finally:

            time.sleep(random.randint(1, 2))

    # 回复推文
    def tweet_with_replay(self, path, account_info):

        cookies = {}

        _account_access = AccountsAccess()

        task_info = {
            "task_type": TaskType.TASK_REPLY,
            "task_status": None,
            "task_info": account_info['content'],
            "task_url": account_info['url'],
            "execute_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        account_info = JsonTool.read_json_file(path)

        if isinstance(account_info, dict) and "cookies" in account_info:
            for _cookie in account_info['cookies']:
                if _cookie["name"] in ["ct0", "auth_token"]:
                    cookies[_cookie["name"]] = _cookie["value"]

        task = {
            "task_file": path,
            "task_info": task_info,
            "cookies": account_info["cookies"],
            "account_type": account_info["activity_params"]["type"]
        }

        process_object = None

        def check_status(response_status, task_file_path):

            if response_status == ResponseCode.FORBIDDEN:
                _account_access.forbidden_account(task_file_path)
                logging.info("账号已锁定，禁用账号文件：{}".format(task_file_path))

        if not process_object:
            logging.info("进入process_object")
            process_object = CustomSocialActions()
            if not process_object.set_cookies(task["cookies"]):
                _account_access.forbidden_account(task["task_file"])
                logging.info("账号Cookies不可用，禁用账号文件：{}".format(task["task_file"]))
                return 2, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])

        try:

            task["task_info"]["execute_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if task["task_info"]["task_type"] == TaskType.TASK_REPLY:

                replay_status, replay_response = self.api_reply(
                    task["task_info"]["task_info"], task["task_info"]["task_url"], cookies, path
                )
                task["task_info"]["task_status"] = replay_status
                _account_access.add_behavior_track(task["task_file"], task["task_info"])
                check_status(replay_status, task["task_file"])
                logging.info("处理任务类型：{}，处理结果：{}".format(task["task_info"]["task_type"], task["task_info"]))
                return replay_status, replay_response

            else:

                logging.error("未知任务类型：{}".format(task["task_info"]["task_type"]))
                return ResponseCode.EXCEPTION, "未知任务类型：{}".format(task["task_info"]["task_type"])
        except Exception as msg:

            logging.exception("任务:{}，处理异常，异常信息：{}".format(task, msg))
            return ResponseCode.EXCEPTION, msg
        finally:

            time.sleep(random.randint(1, 2))

    # 转发推文
    def tweet_with_retweet(self, path, account_info):

        cookies = {}

        _account_access = AccountsAccess()

        task_info = {
            "task_type": TaskType.TASK_RETWEET,
            "task_status": None,
            "task_info": account_info['content'],
            "task_url": account_info['url'],
            "execute_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        account_info = JsonTool.read_json_file(path)

        if isinstance(account_info, dict) and "cookies" in account_info:
            for _cookie in account_info['cookies']:
                if _cookie["name"] in ["ct0", "auth_token"]:
                    cookies[_cookie["name"]] = _cookie["value"]

        task = {
            "task_file": path,
            "task_info": task_info,
            "cookies": account_info["cookies"],
            "account_type": account_info["activity_params"]["type"]
        }

        process_object = None

        def check_status(response_status, task_file_path):

            if response_status == ResponseCode.FORBIDDEN:
                _account_access.forbidden_account(task_file_path)
                logging.info("账号已锁定，禁用账号文件：{}".format(task_file_path))

        if not process_object:
            logging.info("进入process_object")
            process_object = CustomSocialActions()
            if not process_object.set_cookies(task["cookies"]):
                _account_access.forbidden_account(task["task_file"])
                logging.info("账号Cookies不可用，禁用账号文件：{}".format(task["task_file"]))
                # return ResponseCode.EXCEPTION, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])
                return 2, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])

        try:

            task["task_info"]["execute_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if task["task_info"]["task_type"] == TaskType.TASK_RETWEET:

                retweet_status, retweet_response = self.api_retweet(
                    task["task_info"]["task_info"], task["task_info"]["task_url"], cookies, path
                )
                task["task_info"]["task_status"] = retweet_status
                _account_access.add_behavior_track(task["task_file"], task["task_info"])
                check_status(retweet_status, task["task_file"])
                logging.info("处理任务类型：{}，处理结果：{}".format(task["task_info"]["task_type"], task["task_info"]))
                return retweet_status, retweet_response

            else:

                logging.error("未知任务类型：{}".format(task["task_info"]["task_type"]))
                return ResponseCode.EXCEPTION, "未知任务类型：{}".format(task["task_info"]["task_type"])
        except Exception as msg:

            logging.exception("任务:{}，处理异常，异常信息：{}".format(task, msg))
            return ResponseCode.EXCEPTION, msg
        finally:

            time.sleep(random.randint(1, 2))

    # 关注（指定）
    def tweet_with_follow_appoint(self, path, account_info):

        cookies = {}

        _account_access = AccountsAccess()

        task_info = {
            "task_type": TaskType.TASK_FOLLOW_APPOINT,
            "task_status": None,
            "task_info": account_info['url'],
            "execute_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        account_info = JsonTool.read_json_file(path)

        if isinstance(account_info, dict) and "cookies" in account_info:
            for _cookie in account_info['cookies']:
                if _cookie["name"] in ["ct0", "auth_token"]:
                    cookies[_cookie["name"]] = _cookie["value"]

        task = {
            "task_file": path,
            "task_info": task_info,
            "cookies": account_info["cookies"],
            "account_type": account_info["activity_params"]["type"]
        }

        process_object = None

        def check_status(response_status, task_file_path):

            if response_status == ResponseCode.FORBIDDEN:
                _account_access.forbidden_account(task_file_path)
                logging.info("账号已锁定，禁用账号文件：{}".format(task_file_path))

        if not process_object:
            logging.info("进入process_object")
            process_object = CustomSocialActions()
            if not process_object.set_cookies(task["cookies"]):
                _account_access.forbidden_account(task["task_file"])
                logging.info("账号Cookies不可用，禁用账号文件：{}".format(task["task_file"]))
                # return ResponseCode.EXCEPTION, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])
                return 2, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])

        try:

            task["task_info"]["execute_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if task["task_info"]["task_type"] == TaskType.TASK_FOLLOW_APPOINT:

                follow_appoint_status, follow_appoint_response = self.api_follow(
                    task["task_info"]["task_info"], cookies, path
                )
                task["task_info"]["task_status"] = follow_appoint_status
                _account_access.add_behavior_track(task["task_file"], task["task_info"])
                check_status(follow_appoint_status, task["task_file"])
                logging.info("处理任务类型：{}，处理结果：{}".format(task["task_info"]["task_type"], task["task_info"]))
                return follow_appoint_status, follow_appoint_response

            else:

                logging.error("未知任务类型：{}".format(task["task_info"]["task_type"]))
                return ResponseCode.EXCEPTION, "未知任务类型：{}".format(task["task_info"]["task_type"])
        except Exception as msg:

            logging.exception("任务:{}，处理异常，异常信息：{}".format(task, msg))
            return ResponseCode.EXCEPTION, msg
        finally:

            time.sleep(random.randint(1, 2))

    # 关注（自动）
    def tweet_with_follow_auto(self, path, account_info):

        cookies = {}

        _account_access = AccountsAccess()

        task_info = {
            "task_type": TaskType.TASK_FOLLOW_AUTO,
            "task_status": None,
            "task_info": account_info['count'],
            "execute_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        account_info = JsonTool.read_json_file(path)

        if isinstance(account_info, dict) and "cookies" in account_info:
            for _cookie in account_info['cookies']:
                if _cookie["name"] in ["ct0", "auth_token"]:
                    cookies[_cookie["name"]] = _cookie["value"]

        task = {
            "task_file": path,
            "task_info": task_info,
            "cookies": account_info["cookies"],
            "account_type": account_info["activity_params"]["type"]
        }

        process_object = None

        def check_status(response_status, task_file_path):

            if response_status == ResponseCode.FORBIDDEN:
                _account_access.forbidden_account(task_file_path)
                logging.info("账号已锁定，禁用账号文件：{}".format(task_file_path))

        if not process_object:
            logging.info("进入process_object")
            process_object = CustomSocialActions()
            if not process_object.set_cookies(task["cookies"]):
                _account_access.forbidden_account(task["task_file"])
                logging.info("账号Cookies不可用，禁用账号文件：{}".format(task["task_file"]))
                # return ResponseCode.EXCEPTION, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])
                return 2, "账号Cookies不可用，禁用账号文件：{}".format(task["task_file"])

        try:

            task["task_info"]["execute_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if task["task_info"]["task_type"] == TaskType.TASK_FOLLOW_AUTO:

                follow_auto_status, follow_auto_response = self.api_follow_auto(
                    task["task_info"]["task_info"], cookies, path
                )
                print('1111111111111111')
                print(follow_auto_status, follow_auto_response)
                task["task_info"]["task_status"] = follow_auto_status
                print('22222222222222222222222')
                print(task["task_file"], task["task_info"])
                _account_access.add_behavior_track(task["task_file"], task["task_info"])
                check_status(follow_auto_status, task["task_file"])
                logging.info("处理任务类型：{}，处理结果：{}".format(task["task_info"]["task_type"], task["task_info"]))
                return follow_auto_status, follow_auto_response

            else:

                logging.error("未知任务类型：{}".format(task["task_info"]["task_type"]))
                return ResponseCode.EXCEPTION, "未知任务类型：{}".format(task["task_info"]["task_type"])
        except Exception as msg:

            logging.exception("任务:{}，处理异常，异常信息：{}".format(task, msg))
            return ResponseCode.EXCEPTION, msg
        finally:

            time.sleep(random.randint(1, 2))

