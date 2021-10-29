import copy
import json
import logging
import random
import socket
import struct
import threading
import time
import ObtainSocial
import ObtainLogin
from threading import Lock as _Lock
from Utils.cryptotool import CryptoTool
from core.setting import AppType
from socketServer.Utils import RetCode, MsgType, MsgInfoHead, SocketServerInfo
from Utils.JsonTool import JsonTool

static_re_content = ""
static_thread_id = ""
static_msg_id = ""


class ProcessThread(threading.Thread):
    # global static_re_content
    # global static_thread_id
    # global static_msg_id

    def __init__(self, request, address, task_queue):
        super().__init__()
        self.runTime = True
        self.request = request
        self.address = address
        self._logger = logging.getLogger()
        self._head_size = struct.calcsize('!IIIQ')
        self._task_queue = task_queue
        self.connect_info = SocketServerInfo()  # 存储Socket建链信息
        self._locker = _Lock()

    def _init(self):
        self.request.settimeout(360)
        self.thread_id = threading.currentThread().ident
        logging.info(u"ClientThread[{}]处理客户端连接线程：初始化完成!".format(self.thread_id))

    def _receive_all(self, buffer_size, permit_timeouts=3, chunk_size=10240000000):
        """
        接收指定字节数的数据
        :param buffer_size: 接收字节数
        :param permit_timeouts: 允许超时次数
        :param chunk_size: 单次接收大小
        :return: 返回接收数据
        """
        body_data = b""
        if buffer_size <= 0:
            self._logger.error(u"ClientThread[{}]接收数据大小错误，接收大小：{}".format(
                threading.currentThread().getName(), buffer_size))
            return RetCode.SUCCESS, body_data

        remain_len = buffer_size  # 16600264
        _timeouts = 0
        receive_data = b''
        if remain_len > 0:
            try:
                receive_size = chunk_size if remain_len > chunk_size else remain_len
                try:
                    receive_res = receive_size % 102400
                    receive_count = receive_size // 102400
                    for i in range(receive_count):
                        data = self.request.recv(102400, socket.MSG_WAITALL)
                        receive_data += data
                    receive_data += self.request.recv(receive_res, socket.MSG_WAITALL)
                    if receive_data == b'':
                        self.runTime = False
                        return RetCode.NETWORK_ERROR, None
                except Exception as ex:
                    self._logger.info(u'没有接收带数据，异常报错处理: {}'.format(ex))
                    self.runTime = False
                    return RetCode.NETWORK_ERROR, None

                if not receive_data:
                    return RetCode.NETWORK_ERROR, body_data
                body_data += receive_data
                remain_len = buffer_size - len(body_data)
            except socket.timeout:
                return RetCode.TIMEOUT_ERROR, body_data
            except socket.error as msg:
                self._logger.exception(u'ClientThread[{}]数据接收出错，错误信息：{}'.format(
                    threading.currentThread().getName(), msg))
                return RetCode.NETWORK_ERROR, body_data
            except Exception as msg:
                self._logger.exception(u'ClientThread[{}]接收数据异常，异常信息：{}'.format(
                    threading.currentThread().getName(), msg))
                return RetCode.OTHER_ERROR, body_data
        self._logger.info("ClientThread[{}] 成功接收数据，长度：{}".format(
            threading.currentThread().getName(), len(body_data)))
        return RetCode.SUCCESS, body_data  # 返回是接收的状态和请求体数据

    def close_client(self):
        """
        关闭客户链接
        :return:
        """
        try:
            if self.connect_info.connect == self.request:
                self.update_socket_info(None, "")
                # self.request.close()
            if hasattr(self.request, 'close'):
                self.request.close()
        except Exception as msg:
            self._logger.error(u'ClientThread[{}]客户端关闭异常，异常信息：{}'.format(self.thread_id, msg))

    def update_socket_info(self, client, addr):
        """
        更新客户端信息
        :param client: 客户端链接通道
        :param addr: 客户端地址
        """
        with self._locker:
            if self.connect_info.connect != client or self.connect_info.address != addr:
                self.connect_info.connect = client
                self.connect_info.address = addr

    def _receive_header(self):
        return self._receive_all(self._head_size, permit_timeouts=2)  # permit_timeouts数据超时次数

    def _send_all(self, msg_id, content):
        """给java发送数据"""
        if content is not None:
            try:
                self.request.sendall(content)
            except socket.timeout:
                self._logger.error(u'任务请求消息发送超时')
                return RetCode.TIMEOUT_ERROR
            except socket.error:
                self._logger.error(u'客户端连接已关闭')
                return RetCode.NETWORK_ERROR
            else:
                self._logger.info(u'消息发送成功，消息id【{}】'.format(msg_id))
                return RetCode.SUCCESS

    def _send_heart_beat(self, msgid, msgtype, msglen):
        _head = MsgInfoHead()
        _head.msg_id = msgid
        _head.msg_type = msgtype
        _head.msg_len = msglen
        _head.time_stamp = int(time.time())
        data = (_head.msg_id, _head.msg_type, _head.msg_len, _head.time_stamp)
        dataByte = struct.pack('!IIIQ', *data)
        self._logger.info(u'回复心跳响应{}'.format(dataByte))
        self.request.sendall(dataByte)

    def _decrypt_msg(self, data):
        """
        解密
        :param data:
        :return:
        """
        try:
            aes_text = data[:-16]
            # key是后16位
            AES_KEY = data[-16:]
            info = CryptoTool(AES_KEY).decrypt(aes_text)
            # print("解密后: ", str(info, 'utf-8'), type(str(info)), type(info))
            info_str = str(info, 'utf-8')
            # self._logger.debug(u"ClientThread[{}] 接收到客户端消息体, 内容：{}".format(
            #     threading.currentThread().getName(), info_str))
            return RetCode.SUCCESS, info_str
        except Exception as msg:
            self._logger.exception(u"ClientThread[{}] 加解密异常, 异常内容：{}".format(
                threading.currentThread().getName(), msg))
            return RetCode.PARSE_ERROR, ''

    # def _encrypt_msg(self, data):
    #     try:
    #         # _content = JSONEncoder(ensure_ascii=False, sort_keys=True).encode(data)
    #         _content = CryptoTool().encrypt(data)
    #         return RetCode.SUCCESS, _content
    #     except Exception as msg:
    #         self._logger.exception(u"ClientThread[{}] 加解密异常, 异常内容：{}".format(
    #             threading.currentThread().getName(), msg))

    def _encrypt_msg(self, data):
        """
        加密
        :param data:
        :return:
        """
        try:
            # key是s随机16位
            # json的body进行加密
            AES_KEY = self.generate_random_str()
            logging.info("AES_KEY类型为:{}，AES_KEY内容为:{}".format(type(AES_KEY), AES_KEY))
            # AES_KEY = data[-16:]
            # _content = JSONEncoder(ensure_ascii=False, sort_keys=True).encode(data)
            # _content = CryptoTool(AES_KEY).encrypt(data)
            _content = CryptoTool(AES_KEY).encrypt_from_dict_data(data)
            print("加密类型为：{},加密内容为：{}".format(type(_content), _content))
            _content = str(_content, 'utf-8') + AES_KEY
            print("str过后加密类型为：{},加密内容为：{}".format(type(_content), _content))
            return RetCode.SUCCESS, _content
        except Exception as msg:
            self._logger.exception(u"ClientThread[{}] 加解密异常, 异常内容：{}".format(
                threading.currentThread().getName(), msg))
            return RetCode.PARSE_ERROR, ''

    def generate_random_str(self, randomlength=16):
        """
        生成一个指定长度的随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    # def build_msg(self, msg_type, msg_body, msg_id):
    #     """重新构造发送给java的数据流"""
    #     _head = MsgInfoHead()
    #     _head.msg_id = msg_id
    #     _head.msg_type = msg_type
    #     _head.time_stamp = int(time.time())
    #     state, _content = RetCode.SUCCESS, msg_body
    #     _head.msg_len = self._head_size + len(json.dumps(_content).encode('utf8'))
    #     try:
    #         content = struct.pack('!IIIQ{}s'.format(len(json.dumps(_content).encode('utf8'))), _head.msg_id,
    #                               _head.msg_type, _head.msg_len, _head.time_stamp, json.dumps(_content).encode('utf8'))
    #         self._logger.debug(u'ClientThread[{}] 上传消息体构造成功，消息类型{},消息内容：{}'.format(
    #             threading.currentThread().getName(), hex(msg_type), msg_body))
    #         return content, _head.msg_id
    #     except Exception as msg:
    #         self._logger.exception(u'ClientThread[{}] 上传消息体构造失败，消息类型{},错误消息{}'.format(
    #             threading.currentThread().getName(), hex(msg_type), msg))
    #         return None, None

    def build_msg(self, msg_type, msg_body, msg_id):
        """重新构造发送给java的数据流"""
        _head = MsgInfoHead()
        _head.msg_id = msg_id
        _head.msg_type = msg_type
        _head.time_stamp = int(time.time())
        state, _content = RetCode.SUCCESS, msg_body

        # 加密 _content（dict）
        status, _content = self._encrypt_msg(_content)
        print(status, _content)
        # _head.msg_len = self._head_size + len(json.dumps(_content).encode('utf8'))
        _head.msg_len = self._head_size + len(_content.encode('utf8'))
        try:
            # content = struct.pack('!IIIQ{}s'.format(len(json.dumps(_content).encode('utf8'))), _head.msg_id,
            #                       _head.msg_type, _head.msg_len, _head.time_stamp, json.dumps(_content).
            #                       encode('utf8'))

            content = struct.pack('!IIIQ{}s'.format(len(_content.encode('utf8'))), _head.msg_id,
                                  _head.msg_type, _head.msg_len, _head.time_stamp, _content.encode('utf8'))
            self._logger.debug(u'ClientThread[{}] 上传消息体构造成功，消息类型{},消息内容：{}'.format(
                threading.currentThread().getName(), hex(msg_type), msg_body))
            return content, _head.msg_id
        except Exception as msg:
            self._logger.exception(u'ClientThread[{}] 上传消息体构造失败，消息类型{},错误消息{}'.format(
                threading.currentThread().getName(), hex(msg_type), msg))
            return None, None

    def _process_task_request(self, msg_header, msgType):
        state_body, data = self._receive_all(msg_header.msg_len - self._head_size)
        if RetCode.SUCCESS == state_body:
            state, content = RetCode.SUCCESS, data
            if state != RetCode.SUCCESS:
                return False
            else:
                getData = {}
                # logging.info("源数据类型为:{},数据为:{}".format(type(content), content))
                content = content.decode('utf8')
                # logging.info("decode源数据类型为:{},数据为:{}".format(type(content), content))
                # 解密body
                status, content = self._decrypt_msg(content)
                logging.info("状态为:{}".format(status))
                if 0 != status:
                    msg_body = {
                        "data": {
                            "code": 5,
                            "msg": "数据异常,解密失败"
                        }
                    }
                    re_content, msg_id = self.build_msg(msgType, msg_body, msg_header.msg_id)
                    self._send_all(msg_id, re_content)
                    return False

                if hex(msgType) == '0x10010001':  # 登录响应
                    # 判断执行登录
                    # getData = {}
                    try:
                        getData = eval(json.loads(content)['data'])
                        # getData = eval(json.loads(content.decode('utf8'))['data'])
                        appId = getData['appId']
                        phone = getData['phone']
                        aes_pwd = getData['pwd']
                        # print(type(aes_pwd))
                        acct = getData['acct']
                        self._logger.info("接收数据appId,acct为：{},{}".format(appId, acct))
                        status, pwd = self._decrypt_msg(aes_pwd)
                        print(pwd)
                        if 0 == status:
                            status, msg = ObtainLogin.login_begin(appId, phone, pwd, acct)
                            msg_body = {
                                "data": {
                                    "code": status,
                                    "msg": msg
                                }
                            }
                            re_content, msg_id = self.build_msg(msgType, msg_body, msg_header.msg_id)
                            self._send_all(msg_id, re_content)
                            return True
                        else:
                            msg_body = {
                                "data": {
                                    "code": 5,
                                    "msg": "数据异常,解密失败"
                                }
                            }
                            re_content, msg_id = self.build_msg(msgType, msg_body, msg_header.msg_id)
                            self._send_all(msg_id, re_content)
                            return False

                    except Exception as e:
                        self._logger.error(u'用户登录异常报错:{},'.format(e))
                        msg_body = {
                            "data": {
                                "code": 5,
                                "msg": "数据异常:{}".format(getData)
                            }
                        }
                        re_content, msg_id = self.build_msg(msgType, msg_body, msg_header.msg_id)
                        self._send_all(msg_id, re_content)
                        return False

                elif hex(msgType) == '0x10010003':  # 发布论坛帖子响应
                    # getData = {}
                    try:
                        getData = eval(json.loads(content)['data'])
                        # getData = eval(json.loads(content.decode('utf8'))['data'])
                        appId = getData['appId']
                        acct = getData['acct']
                        title = getData['title']
                        contents = getData['content']
                        postUrl = getData['postUrl']
                        fileNames = getData['fileNames']
                        fileBytes = getData['fileBytes']
                        status, msg = ObtainSocial.tweet_begin(appId, acct, title, contents, postUrl,
                                                               fileNames, fileBytes)
                        # TODO status, msg = 发布推文脚本(appId, acct, title, contents, postUrl, fileNames, fileBytes)
                        msg_body = {
                            "data": {
                                "code": status,
                                "msg": msg
                            }
                        }
                        re_content, msg_id = self.build_msg(msgType, msg_body, msg_header.msg_id)
                        global static_re_content
                        global static_thread_id
                        global static_msg_id
                        static_re_content = re_content
                        static_msg_id = msg_id
                        static_thread_id = threading.currentThread().ident
                        print("发布论坛成功")
                        print(static_re_content)
                        print(static_msg_id)
                        print(static_thread_id)
                        self._send_all(msg_id, re_content)
                        return True

                    except Exception as e:
                        self._logger.error(u'用户发布推文异常报错{}'.format(e))
                        msg_body = {
                            "data": {
                                "code": 5,
                                "msg": "数据异常:{}".format(getData['appId'], getData['acct'], getData['content'],
                                                        getData['fileNames'], len(getData['fileBytes']))
                            }
                        }
                        re_content, msg_id = self.build_msg(msgType, msg_body, msg_header.msg_id)
                        # global static_re_content
                        # global static_thread_id
                        # global static_msg_id
                        static_re_content = re_content
                        static_msg_id = msg_id
                        static_thread_id = threading.currentThread().ident
                        print("发布论坛失败")
                        print(static_re_content)
                        print(static_msg_id)
                        print(static_thread_id)
                        self._send_all(msg_id, re_content)
                        return False

    @staticmethod
    def _parse_header(data):
        """解析从java获取的数据的请求头信息"""
        if len(data) == 20:
            msg_header_tuple = struct.unpack_from('!IIIQ', data)
            msg_header = MsgInfoHead()
            msg_header.msg_id = msg_header_tuple[0]
            msg_header.msg_type = msg_header_tuple[1]
            msg_header.msg_len = msg_header_tuple[2]
            print('####', msg_header.msg_len)
            msg_header.time_stamp = msg_header_tuple[3]
            return msg_header
        else:
            return None

    def run(self):
        # global static_re_content
        # global static_thread_id
        # global static_msg_id
        try:
            # self._init()
            while self.runTime:
                print("进入循环接收数据")

                global static_re_content
                global static_thread_id
                global static_msg_id
                print(static_re_content)
                print(static_msg_id)
                print(static_thread_id)
                if static_re_content is not '' and static_thread_id != threading.currentThread().ident:
                    self._send_all(static_msg_id, static_re_content)
                    static_re_content = ""
                    static_msg_id = ""
                    static_thread_id = ""

                # self.request.settimeout(10)
                # self.request.settimeout(10)
                # self.request.settimeout(10)
                state_head, data_head = self._receive_header()

                # 如果成功进行处理请求头
                if state_head == RetCode.SUCCESS:
                    msg_header = self._parse_header(data_head)
                    if msg_header is not None:
                        # 如果是心跳响应
                        if msg_header.msg_type == MsgType.Heart_request:
                            self._logger.info(u'进入心跳响应')
                            msg_header.msg_type = MsgType.Heart_response
                            self._send_heart_beat(msg_header.msg_id, msg_header.msg_type, msg_header.msg_len)
                        # 如果请求头的类型是账号登录验证请求
                        elif msg_header.msg_type == MsgType.Account_Task_request:
                            self._logger.info(u'进入账号登录')
                            msg_header.msg_type = MsgType.Account_response
                            self._process_task_request(msg_header, msg_header.msg_type)
                        # 如果请求头的类型是发布推文任务请求
                        elif msg_header.msg_type == MsgType.Tweet_Task_request:
                            self._logger.info(u'进入发布论坛帖子任务')
                            msg_header.msg_type = MsgType.Tweet_response
                            self._process_task_request(msg_header, msg_header.msg_type)

                        else:
                            self._logger.error("接收到消息头，消息类型【{}】未知".format(msg_header.msg_type))
                else:
                    self._logger.error("消息头为空, 等待请求任务...")
                    # break
        except Exception as msg:
            self._logger.exception(u"客户端连接异常，异常信息：{}".format(msg))
        finally:
            # self.close_client()
            if isinstance(self.request, socket.socket):
                self.request = None



class SocketServer(threading.Thread):
    """
    socket 服务线程
    """

    def __init__(self, name, server_ip, server_port, task_queue):
        threading.Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port = server_port
        self.task_queue = task_queue
        self.name = name

    def run(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.server_ip, self.server_port))

            logging.info(u"服务端启动，监听地址{}:{}".format(self.server_ip, self.server_port))
            server.listen(1000)
            while True:
                client, address = server.accept()
                logging.debug(u'客户端:{} 请求连接成功，处理请求'.format(address))
                args = (client, address, self.task_queue)
                socket_thread = ProcessThread(*args)
                # socket_thread.setDaemon(True)
                socket_thread.start()
        except Exception as msg:
            logging.exception(u"服务端启动异常，异常信息：{}".format(msg))
