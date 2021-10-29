#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os
import sys
import logging.handlers
from logging import Logger, getLogger, basicConfig
from logging.config import dictConfig, fileConfig
from Utils import singleton
from logging import StreamHandler as CustomStreamHandler, FileHandler as CustomFileHandler
from logging.handlers import RotatingFileHandler as CustomRotatingFileHandler, \
    TimedRotatingFileHandler as CustomTimedRotatingFileHandler
from Utils.utils import get_absolute_path


class CustomHandlers(object):
    """Logging handlers."""

    stream_handler = CustomStreamHandler  # 日志输出倒流
    file_handler = CustomFileHandler  # 日志输出到文件
    rotating_file_handler = CustomRotatingFileHandler  # 日志文件按大小回滚
    timed_rotating_file_handler = CustomTimedRotatingFileHandler  # 日志文件按时间回滚


class Formatter(object):
    """Logging formatter."""

    format_01 = '%(asctime)-20s %(levelname)-9s %(module)-s %(lineno)5d: %(message)s'
    format_02 = '%(asctime)-20s'


class Datefmt(object):
    """Logging date format."""

    date_fmt_01 = '%Y-%m-%d %H:%M:%S'
    date_fmt_02 = '%a, %d %b %Y %H:%M:%S'


@singleton
class LoggerSingleton(Logger):
    """Logging manager."""

    def __init__(self, name="root", level=logging.DEBUG):
        super().__init__(name, level)

    def init_custom(self, name='', file='', _bytes=10 * 1024 * 1024, _count=7, _level=logging.DEBUG, encrypt_bool=True):
        if name:
            self.name = name
        _file = file if file else "./run.log"
        _absolute_file = get_absolute_path(_file)
        if not os.path.exists(os.path.dirname(_absolute_file)):
            os.makedirs(os.path.dirname(_absolute_file))
        _rotating_file_args = (_absolute_file, 'a', _bytes, _count)
        _stream_args = (sys.stdout,)
        self.setLevel(logging.DEBUG)
        self.propagate = True  # 消息往更高级别的地方传递
        # 日志输出到文件
        rotating_file_handler = CustomHandlers.rotating_file_handler(*_rotating_file_args) if encrypt_bool \
            else logging.handlers.RotatingFileHandler(*_rotating_file_args)  # 切割日志
        rotating_file_handler.setLevel(_level)
        rotating_file_formatter = logging.Formatter(Formatter.format_01, Datefmt.date_fmt_01)
        rotating_file_handler.setFormatter(rotating_file_formatter)
        self.addHandler(rotating_file_handler)
        # 日志打印到控制台
        stream_handler = CustomHandlers.stream_handler(*_stream_args) if encrypt_bool \
            else logging.StreamHandler(*_stream_args)
        stream_handler.setLevel(self.level)
        stream_formatter = logging.Formatter(Formatter.format_01, Datefmt.date_fmt_01)
        stream_handler.setFormatter(stream_formatter)
        self.addHandler(stream_handler)

    @staticmethod
    def init_basic_config(**kwargs):
        basicConfig(**kwargs)

    @staticmethod
    def init_dict_config(dict_config):
        dictConfig(config=dict_config)

    @staticmethod
    def init_file_config(fname, defaults=None, disable_existing_loggers=True):
        fileConfig(fname, defaults=defaults, disable_existing_loggers=disable_existing_loggers)

    @staticmethod
    def get_logger(name="root"):
        return getLogger(name)

    def __reduce__(self):
        return getLogger, ()
