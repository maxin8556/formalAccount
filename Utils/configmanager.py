#!/usr/bin/env python
# -*- coding: utf-8 -*-




import threading
import configparser
from Utils import singleton


@singleton
class ConfigParseSingleton(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        print("__init__")

    def init(self, filename, encoding="utf-8"):
        self.read(filename, encoding=encoding)


# class ConfigParseSingleton(configparser.ConfigParser):
#     _instance_lock = threading.Lock()
#
#     def __init__(self, *args, **kwargs):
#         print("__init__")
#         super().__init__()
#
#     @classmethod
#     def get_instance(cls, *args, **kwargs):
#         if not hasattr(ConfigParseSingleton, '_instance'):
#             with ConfigParseSingleton._instance_lock:
#                 if not hasattr(ConfigParseSingleton, '_instance'):
#                     ConfigParseSingleton._instance = ConfigParseSingleton(*args, **kwargs)
#
#         return ConfigParseSingleton._instance
#
#     def init(self, filename, encoding="utf-8"):
#         self.read(filename, encoding=encoding)


# if __name__ == "__main__":
#
#     ConfigParseSingleton().init(filename="./etc/config.cfg")
#     print(ConfigParseSingleton().get("BREAD_PROXY", "culture"))
