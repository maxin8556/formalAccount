#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os
import json
import logging
import logging.config


class JsonTool(object):

    @staticmethod
    def dict_to_str(obj_json, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False):
        """
        JSON数据类型（List, dict）转为Json字符串
        :param obj_json: JSON类型数据
        :param sort_keys: 分类键
        :param indent: 缩进间隔
        :param separators: 分割符号
        :param ensure_ascii: 转义非ASCII字符，False可以返回UNICODE
        :return: 成功，返回Json字符串；失败，返回None
        """
        if not obj_json:
            logging.error(u"字典类型转Json格式字符串输入错误：不能为空。")
            return None
        try:
            return json.dumps(obj_json, ensure_ascii=ensure_ascii, sort_keys=sort_keys, indent=indent, separators=separators)
        except Exception as msg:
            logging.exception(u"字典类型转Json格式字符串异常，字典{}，异常信息：{}".format(obj_json, msg))
            return None

    @staticmethod
    def str_to_dict(str_json, encoding=None):
        """
        Json字符串转为JSON数据类型（List, dict）
        :param str_json: Json字符串
        :param encoding: 编码格式
        :return: 成功，返回JSON类型数据；失败，返回None
        """
        if not str_json:
            logging.error(u"Json字符串转字典类型输入错误：空")
            return None
        try:
            return json.loads(str_json, encoding=encoding)
        except Exception as msg:
            logging.exception(u"Json字符串转字典类型异常，Json字符串{}，异常信息：{}".format(str_json, msg))
            return None

    @staticmethod
    def write_json_file(obj_json, file_name, save_path=os.getcwd(), ensure_ascii=False):
        """
        Json结构数据写入文件
        :param obj_json: JSON类型数据
        :param file_name: 文件名
        :param save_path: 保存路径
        :param ensure_ascii: 转义非ASCII字符，False可以返回UNICODE
        :return: 成功，返回Ture；失败，返回False
        """
        if not obj_json:
            logging.error(u"写Json文件传入参数错误：JSON类型数据为空")
            return False
        if not file_name:
            logging.error(u"写Json文件传入参数错误：Json文件名为空")
            return False
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        try:
            file_path = os.path.join(save_path, file_name)
            with open(file_path, "w", encoding="utf-8") as f_json:
                json.dump(obj_json, f_json, ensure_ascii=ensure_ascii, sort_keys=True, indent=4, separators=(',', ': '))
            return True
        except Exception as msg:
            logging.exception(u"Json类型数据写入Json文件异常，异常信息：{}".format(msg))
            return False

    @staticmethod
    def read_json_file(file_path, encoding=None, object_hook=None):
        """
        读取Json文件数据
        :param file_path: 文件路径
        :param encoding: 编码格式
        :return: 成功，返回JSON类型数据；失败，返回None
        """
        if not os.path.isfile(file_path):
            logging.error(u"读取Json文件传入参数错误：文件路径不存在")
            return None
        try:
            with open(file_path, 'r', encoding="utf-8") as f_json:
                return json.load(f_json, encoding=encoding, object_hook=object_hook)
        except Exception as msg:
            logging.exception(u"读取Json类型数据异常，异常信息：{}".format(msg))
            return None


class DictDecode:
    """Dict decode class."""

    @classmethod
    def decode_list(cls, data):
        """
        Convert list value encoding to 'utf-8'.
        :param data: list
        :return: list
        """
        rv = []
        for item in data:
            if isinstance(item, bytes):
                item = item.decode('utf-8')
            elif isinstance(item, list):
                item = cls.decode_list(item)
            elif isinstance(item, dict):
                item = cls.decode_dict(item)
            rv.append(item)
        return rv

    @classmethod
    def decode_dict(cls, data):
        """
        Convert dict key-value pair encoding to 'utf-8'.
        :param data: dict
        :return: dict
        """
        rv = {}
        for key, value in data.items():
            if isinstance(key, bytes):
                key = key.decode('utf-8')
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            elif isinstance(value, list):
                value = cls.decode_list(value)
            elif isinstance(value, dict):
                value = cls.decode_dict(value)
            rv[key] = value
        return rv


if __name__ == "__main__":
    print(JsonTool.read_json_file("../result/_AndyTheo__followers_1583771466_0.json", encoding="utf-8"))
    print(JsonTool.read_json_file("../result/_AndyTheo__followers_1583771466_0.json", encoding="utf-8", object_hook=DictDecode.decode_dict))