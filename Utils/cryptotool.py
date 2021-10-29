#!/usr/bin/env python
# -*- coding: utf8 -*-
import json
import base64
from Utils.JsonUTF8 import JsonUTF8Decoder
from Crypto.Cipher import AES


class CryptoTool(object):
    """CryptoTool instances are used to decrypt strings"""

    # def __init__(self, key=None, mode=AES.MODE_ECB):
    #     if key is None:
    #         key = "d$0294f91b6"
    #     if type(key) != bytes:
    #         self.key = key.encode('utf-8')
    #     else:
    #         self.key = key
    #     self.mode = mode
    #     if len(self.key) < AES.block_size:
    #         bs = AES.block_size
    #         while len(self.key) % bs != 0:
    #             self.key += b'\0'

    def __init__(self, key=None, mode=AES.MODE_CBC):

        self.IV = "1234567890123456"
        if key is None:
            key = "1234567890123456"

        self.key = key
        # if type(key) != bytes:
        #     self.key = key.encode('utf-8')
        # else:
        #     self.key = key
        self.mode = mode

    # 加密函数
    def _encrypt(self, text):
        BS = len(self.key)
        pad = lambda s: s + (BS - len(s.encode()) % BS) * chr(BS - len(s.encode()) % BS)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.IV.encode("utf8"))
        self.ciphertext = cryptor.encrypt(bytes(pad(text), encoding="utf8"))
        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(self.ciphertext)

    # 解密函数
    def _decrypt(self, text):
        unpad = lambda s: s[0:-ord(s[-1:])]
        decode = base64.b64decode(text)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.IV.encode("utf8"))
        plain_text = cryptor.decrypt(decode)
        return unpad(plain_text)

    # def _decrypt(self, msg):
    #     """
    #     str内容AES解密
    #     :param msg: 待解密字符串
    #     :return: 返回解密内容
    #     """
    #     if type(msg) != bytes:
    #        msg = msg.encode('utf-8')
    #     bs = AES.block_size
    #     if len(msg) % bs != 0:
    #         return ''
    #     cipher = AES.new(self.key, self.mode)
    #     msg = cipher.decrypt(msg)
    #     if type(msg) == bytes:
    #         msg = msg.decode('utf-8')
    #     return msg.rstrip("\0")
    #
    # def _encrypt(self, msg):
    #     """
    #     str内容AES加密
    #     :param msg: 待加密字符串
    #     :return: 返回加密字符串
    #     """
    #     bs = AES.block_size
    #     cipher = AES.new(self.key, self.mode)
    #     msg = msg.encode('utf-8')
    #     while len(msg) % bs != 0:
    #         msg += b'\0'
    #     return cipher.encrypt(msg)

    def decrypt(self, msg):
        """
        base64+aes解密
        :param msg: 待解密字符串
        :return: 返回解密字符串
        """
        # return self._decrypt(base64.b64decode(msg))
        return self._decrypt(msg)

    def encrypt(self, msg):
        """
        base64+aes加密
        :param msg: 待加密字符串
        :return: 返回加密字符串
        """
        return base64.b64encode(self._encrypt(msg))

    def decrypt_from_dict_string(self, data):
        """
        json加密字串解密
        :param data: 加密字串
        :return: 解密结果字典格式
        """
        return JsonUTF8Decoder().decode(self.decrypt(data))

    def encrypt_from_dict_data(self, dict_data):
        return self._encrypt(json.dumps(dict_data))
