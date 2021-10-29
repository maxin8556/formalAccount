#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os


def convert_path(path: str) -> str:
    return path.replace(r'\/'.replace(os.sep, ''), os.sep)


def get_absolute_path(relative_path: str) -> str:
    return os.path.abspath(relative_path)


def get_relative_path(absolute_path: str) -> str:
    return os.path.realpath(absolute_path)
