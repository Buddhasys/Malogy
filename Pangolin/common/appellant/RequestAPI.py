"""
@author: Albertz
@license: (C) Copyright 2021-2099, Node Supply Chain Manager Corporation Limited.
@contact: Buddha@sys.com
@software: 
@file: RequestAPI.py
@time:
@desc:

"""


from .HttpRequest import HttpRequest
from .WebSocketRequest import WebSocketRequest


class RequestAPI:

    def __init__(self):
        self.__http = HttpRequest()
        self.__ws = WebSocketRequest()

    def request_route(self, req_type=None, sms_type=None, url=None, req_way=None, req_data=None, **kwargs):

        if hasattr(self, f"_{req_type}"):
            if sms_type in ['json'] and req_way in ["post", "put"]:
                return getattr(self, f"_{req_type}")(url, req_way, json=req_data, **kwargs)

            elif sms_type in["xml"]:
                return self.__http.request(url, req_way, data=req_data.encode('utf-8'), **kwargs)

            elif req_way in ['get', 'delete']:
                return self.__http.request(url, req_way, params=req_data, **kwargs)

            elif req_type in ['ws', 'wss']:
                return self.__ws.request(url, req_data, **kwargs)

            else:
                return getattr(self, f"_{req_type}")(url, req_way, data=req_data, **kwargs)
        else:
            raise Exception(f"暂不支持该请求协议类型： {req_type}")

    def _http(self, url, req_way, **kwargs):
        return self.__http.request(url, req_way, **kwargs)

    def _https(self, url, req_way, **kwargs):
        return self.__http.request(url, req_way, **kwargs)

    def _ws(self, url, req_data, **kwargs):
        return self.__ws.request(url, req_data, **kwargs)

    def _wss(self, url, req_data, **kwargs):
        return self.__ws.request(url, req_data, **kwargs)

