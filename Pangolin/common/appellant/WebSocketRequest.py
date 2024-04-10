"""
-------------------------------------------------
        Author :    albertz
        contact:    Buddha@sys.com
      File Name：   WebSocketRequest
           date：   2022/03/09 20:51 上午
   Description :
-------------------------------------------------
   Change Activity:

-------------------------------------------------
"""

import json, logging
import ssl
from uuid import uuid4
import websocket
from GetDictData import GetDictData as Gda

logger=logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
# # 打开日志，便于定位报错
# websocket.enableTrace(True)


class WebSocketRequest:

    def __init__(self):
        """
            连接web服务器
            @:param uri: 服务的url
            @:param timeout: 超时时间
            @:return:
        """
        # 设置超时
        self.__timeout = 0
        # 是否需要验签
        self.__auth = False
        # 取消订阅类型
        self.__unsubTy = None
        # 统计接收的数据
        self.__count = 0
        # 创建ws实例
        self.__ws = None
        # 获取要发送的报文
        self.__message = None
        # 数据容器
        self.__rec = []
        # 是否接收所有数据
        self.__all = True
        # 统计ping的次数
        self.__ping_count = 0
        self.__times = 1
        # 是否verify
        self.__verify = True
        # 鉴权信息
        self.auth_data = None


    def request(self, url, message: dict, auth = False, verify=True, system=None,
                      timeout=10, times=10, unsub=False, all=True, **kwargs):
        """
            http请求
            @param url: 请求地址
            @param req_data: 请求数据
            @param kwargs: 预留
            @return:
        """
        # 设置超时，默认5s
        self.__timeout = timeout
        # 接收传入的数据
        self.__message = message
        # 是否校验
        self.__verify = verify
        # 鉴权数据
        self.auth_data = kwargs
        # 验签
        self.__auth = auth
        # 取消订阅
        self.__unsubTy = unsub
        # 接收所有数据
        self.__all = all
        # 统计ping/pong次数
        self.__times = times
        # 系统
        self.__system = system
        ### 对FUTURE系统url做特殊处理
        if self.__system == "FUTURE":
            sign = self.__get_sign(self.auth_data)
            url += f"?{'&'.join([f'{key}={value}' for key, value in sign.items()])}"
            logger.warning(f"创建连接的数据: \n{sign}")
        # 创建ws实例
        ws = websocket.WebSocketApp(url=url,
                                    on_open=self.on_open,
                                    on_error=self.on_error,
                                    on_message=self.on_message,
                                    on_close=self.on_close,
                                    on_ping=self.on_ping,
                                    on_pong=self.on_pong
                                   )
        # 保持长连接
        ws.run_forever(ping_interval=20,
                       ping_timeout=self.__timeout,
                       sslopt={"cert_reqs": ssl.CERT_NONE},
                       skip_utf8_validation=True
                      )
        # rel.signal(2, rel.abort)
        # rel.dispatch()
        return self.__rec


    def on_open(self, ws):
        """保持连接状态"""
        # 私有需要验签
        if self.__auth and self.__system=="SPOT":
            sign = self.__get_sign(**self.auth_data)
            self.ws_send(ws, sign)
        else:
            pass
        # 开始订阅
        self.ws_send(ws, self.__message)



    def ws_send(self, ws, data):
        """
            发送请求数据体
            :param message: 待发送的数据信息
            :return:
        """
        if not isinstance(data, str):
            data = json.dumps(data)

        logger.info(f"发送数据为 {data}")
        try:
            ws.send(data)
        except Exception as e:
            logger.error(f"socket is already closed.\n detail：{e}")

    def on_ping(self, ws, message):
        """接收服务端返回的ping请求"""
        logger.info(f"Got a ping! A pong reply has already been automatically sent.")

    def on_pong(self, ws, message):
        """接收服务端返回的pong请求"""
        if self.__system == "SPOT":
            ping = {"event": "ping"}
        else:
            ping = {
                "id": str(uuid4()),
                "type": "ping"
            }
        self.ws_send(ws, ping)
        # logger.info(f"Got a pong!")
        self.__ping_count += 1
        if self.__ping_count > self.__times:
            ws.close()

    def on_message(self, ws, message):
        """接收返回的数据"""
        self.__count += 1
        logger.info("*"*66)
        logger.info(f"已接收到第【{self.__count }】条数据: {message}")
        if message and "data" in message:
            self.__rec.append(message)
        # 若不获取所有数据则获得2条数据后退出连接
        if not self.__all and self.__count>2:
            # 不保持连接
            ws.close()
        # 是否取消订阅
        elif self.__unsubTy and self.__count == 8:
            logger.warning("即将取消订阅")
            data = self.__unsubscribe(self.__message)
            self.ws_send(ws, data)
            logger.warning("取消订阅成功")
        if self.__verify and self.__system == "SPOT":  #取消订阅不校验
            pass

    def on_error(self, ws, error):
        """获取报错信息"""
        logger.error(f"ws发生错误：{error}")

    def on_close(self, ws, close_status_code, close_msg):
        """获取关闭连接时的相关信息"""
        logger.info(f"已成功断开连接\nclose_status_code:{close_status_code}\nclose_msg:{close_msg}")


    def __unsubscribe(self, data):
        """根据取消类型获取取消数据"""
        data = {
            "event": "unsubscribe",
            "channel": Gda.get_single_value("channel", self.__message),
            "symbols": Gda.get_single_value("symbols", self.__message)
        }
        if self.__unsubTy == "all":
            data.update({
                "event": "unsubscribe_all"
            })
            return data
        elif self.__system == "FUTURE" and self.__unsubTy:
            self.__message.update({
                "type": "unsubscribe"
            })
            return self.__message
        else:
            return data


    def __get_sign(self, auth_data=None):
        if self.__auth and self.__system == "SPOT":
            data = {
                "event": "subscribe",
                "channel": ["auth"],
                "params": auth_data
            }
        elif self.__system == "FUTURE":
            data = {
                "token": auth_data["token"],
                "connectId": str(uuid4()),
                "acceptUserMessage": self.__auth
            }
        else:
            data = {"event": "subscribe", "channel": ["webAuth"],
                    "params": {
                       "sessionId": "20020",
                       "fingerprint": "test"
                    }
            }
        return data


