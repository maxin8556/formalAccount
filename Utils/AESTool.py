#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2020/1/16 13:28
# @Author: lli
# @Site:
# @File    : bussinessprocess.py
# @Software: PyCharm
#补位方式采用\0 补位，区别于ccp的补位方式
import os
from Crypto.Cipher import AES


class AESTool(object):
    '''aes 加解密'''

    def __init__(self, key, mode=AES.MODE_ECB):
        self.key = key
        self.mode = mode
        if len(self.key) < AES.block_size:
            padding_len = AES.block_size - len(self.key) % AES.block_size
            self.key += '\x00' * padding_len

    def decrypt(self, msg):
        bs = AES.block_size
        if len(msg) % bs != 0:
            return ''
        cipher = AES.new(self.key, self.mode)
        msg = cipher.decrypt(msg).decode()
        return msg.rstrip("\0")

    def decrypt_zero_padding(self, msg):
        bs = AES.block_size
        if len(msg) % bs != 0:
            return ''
        cipher = AES.new(self.key, self.mode)
        msg = cipher.decrypt(msg)
        return msg.rstrip('\x00')

    def decrypt_file(self, fname):
        tmpfile = fname + '.tmp'
        with open(fname, 'rb') as fin, open(tmpfile, 'wb') as fout:
            bs = AES.block_size

            cipher = AES.new(self.key, self.mode)
            chunk = fin.read(1024 * bs)
            while True:
                next_chunk = fin.read(1024 * bs)
                if len(next_chunk) == 0:
                    fout.write(self.decrypt(chunk))
                    break
                else:
                    fout.write(cipher.decrypt(chunk))
                chunk = next_chunk

        os.rename(tmpfile, fname)

    def encrypt(self, msg):
        bs = AES.block_size
        cipher = AES.new(self.key, self.mode)
        if len(msg) == 0 or len(msg) % bs != 0:
            padding_len = (bs - len(msg) % bs) or bs
            msg += '\0' * padding_len
        return cipher.encrypt(msg.encode('ascii', 'ignore'))

    def encrypt_file(self, fname):
        tmpfile = fname + '.tmp'
        with open(fname, 'rb') as fin, open(tmpfile, 'wb') as fout:
            finished = False
            bs = AES.block_size

            cipher = AES.new(self.key, self.mode)
            while not finished:
                chunk = fin.read(1024 * bs)
                if len(chunk) == 0 or len(chunk) % bs != 0:
                    padding_len = (bs - len(chunk) % bs) or bs
                    chunk += chr(padding_len) * padding_len
                    finished = True
                fout.write(cipher.encrypt(chunk))

        os.rename(tmpfile, fname)

    @staticmethod
    def _mkchar(c):
        return chr((c | 0x20) & 0x7F)

    @staticmethod
    def gen_key(key):
        print(key)
        i = 0
        k = ''
        while i < 16:
            k += AESTool._mkchar((ord(key[i * 2]) << 4 & 0xFF) | (ord(key[i * 2 + 1]) & 0x0F))
            i += 1
        return k
