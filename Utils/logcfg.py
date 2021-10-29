#!/usr/bin/env python
# -*- coding: utf-8 -*-


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'form01': {
            'format': '[%(asctime)-20s %(levelname)-9s %(module)-s %(lineno)5d]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'form02': {
            'format': '[%(asctime)-20s %(levelname)-9s %(filename)-s %(lineno)5d]: %(message)s',
            'datefmt': '%a, %d %b %Y %H:%M:%S'
        }
    },
    'handlers': {
        'consolehandler': {
            'class': 'logging.StreamHandler',
            'formatter': 'form01',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        },
        'rotatingfilehandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'form01',
            'level': 'DEBUG',
            'filename': 'run.log',
            'mode': 'a',
            'maxBytes': 10*1024*1024,
            'backupCount': 3,
            "encoding": "utf8"
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['consolehandler', 'rotatingfilehandler']
    }
}
