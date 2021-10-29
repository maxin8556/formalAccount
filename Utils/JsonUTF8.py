#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JsonUTF8Decoder module.

"""

from json import JSONDecoder


class DictDecode(object):
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
            if isinstance(item, str):
                item = item
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
        # python2
        # for key, value in data.iteritems():
        #     if isinstance(key, unicode):
        #         key = key.encode('utf-8')
        #     if isinstance(value, unicode):
        #         value = value.encode('utf-8')
        #     elif isinstance(value, list):
        #         value = cls.decode_list(value)
        #     elif isinstance(value, dict):
        #         value = cls.decode_dict(value)
        #     rv[key] = value
        # return rv

        # python3
        for key, value in data.items():
            if isinstance(key, str):
                key = key
            if isinstance(value, str):
                value = value
            elif isinstance(value, list):
                value = cls.decode_list(value)
            elif isinstance(value, dict):
                value = cls.decode_dict(value)
            rv[key] = value
        return rv


class JsonUTF8Decoder(JSONDecoder):
    """ Convert json string to dict type data, and unicode to 'utf-8'."""

    def __init__(self, encoding=None, object_hook=DictDecode.decode_dict, parse_float=None,
                 parse_int=None, parse_constant=None, strict=True,
                 object_pairs_hook=None):
        JSONDecoder.__init__(self, encoding=encoding, object_hook=object_hook, parse_float=parse_float,
                             parse_int=parse_int, parse_constant=parse_constant, strict=strict,
                             object_pairs_hook=object_pairs_hook)
