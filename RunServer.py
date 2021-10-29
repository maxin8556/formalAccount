import logging
import queue
import time
from core.setting import FileType
from Utils.ThreadManager import ThreadManageTool
from socketServer.socketServer import SocketServer


def main():
    thread_dict = {}
    task_queue = queue.Queue()

    # 创建服务端线程
    server_args = ("Thread_SocketServer", FileType.ip, FileType.port, task_queue)
    # server_args = ("Thread_SocketServer", "10.25.35.132", 20250, task_queue)
    server_thread = SocketServer(*server_args)
    server_thread.setDaemon(True)
    server_thread.start()
    thread_dict[server_thread.name] = (SocketServer, server_args)
    logging.info(u"监听服务端线程启动")

    # 守护线程
    while True:
        ThreadManageTool.guard_thread(thread_dict)
        time.sleep(10)


if __name__ == "__main__":
    from Utils.logcfg import LOGGING_CONFIG
    from Utils.Logger import LoggerSingleton
    LoggerSingleton().init_dict_config(LOGGING_CONFIG)

    try:
        main()
    except Exception as msg:
        logging.exception("异常信息：{}".format(msg))
