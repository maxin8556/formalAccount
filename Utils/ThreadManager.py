#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Desc    : 线程管理模块
'''

import logging
import threading
from concurrent.futures import ThreadPoolExecutor


class ThreadManageTool(object):
    """ThreadManageTool class are used to provide daemon services for threads."""

    @staticmethod
    def active_thread():
        """
        打印当前活动线程
        :return:
        """
        current_active_thread_list = []
        try:
            current_active_thread_list = [th.getName() for th in threading.enumerate()]
        except Exception as msg:
            logging.exception(u'获取当前活动线程列表异常，异常信息：{}'.format(msg))
        finally:
            return current_active_thread_list

    @staticmethod
    def guard_thread(sub_thread_dict):
        """
        守护线程
        :param sub_thread_dict: 线程字典
        :return:
        """
        try:
            current_active_thread_list = ThreadManageTool.active_thread()
            logging.info(u'当前活动线程列表:\n    {}'.format("\n    ".join(current_active_thread_list)))
            # 检测线程是否运行正常
            for thread_name in sub_thread_dict.keys():
                if thread_name not in current_active_thread_list:
                    logging.warning(u'线程【{}】已挂掉，重新拉起。'.format(thread_name))
                    thread_obj, args = sub_thread_dict[thread_name][0], sub_thread_dict[thread_name][1]
                    if callable(thread_obj):
                        th = thread_obj(*args)
                        th.name = thread_name
                        th.setDaemon(True)
                        th.start()
        except Exception as msg:
            logging.exception(u"线程守护异常，异常信息：{}".format(msg))


class ThreadPoolManage(ThreadPoolExecutor):
    """ThreadPoolTool class used to build and manager thread pool."""

    def __init__(self, max_workers=None, thread_name_prefix=''):
        ThreadPoolExecutor.__init__(self, max_workers, thread_name_prefix)

    def task_queue_size(self):
        """Return the approximate size of thread work queue (not reliable!)."""
        return self._work_queue.qsize()

    def task_queue_empty(self):
        """Return True if thread work queue is empty, False otherwise (not reliable!)."""
        return self._work_queue.empty()
