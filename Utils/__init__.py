#!/usr/bin/env python
# -*- coding: utf-8 -*-



from functools import wraps


def singleton(cls, *args, **kw):
    instances = {}

    @wraps(cls)
    def wrapper():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return wrapper
