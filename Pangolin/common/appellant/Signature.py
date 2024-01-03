"""
-------------------------------------------------
        Author :    albertz.yang
        contact:    albertz.yang@poloniex.com
      File Name：   Signature
           date：   2022/3/22 6:57 下午
   Description :
-------------------------------------------------
   Change Activity:
                   2022/3/22:
-------------------------------------------------
"""

import hashlib
import urllib
import urllib.parse
import time
import hmac
import base64
import json, re


class Signature:
    """
    Desc：创建签名
    """

    def __init__(self, apikey=None, keySecret=None, password=None, **kwargs):
        self.__apikey = apikey
        self.__keySecret = keySecret
        self.__password = password
        self.__time = int(time.time() * 1000)
        # 将时间戳转为毫秒，需要参与签名

    def create_sign(self, params: dict, method, path, system):
        timestamp = self.__time
        sign_params = self.__get_sign_params(params, method, path, timestamp)
        # print(encode_params)
        sign_params = sign_params.encode(encoding="UTF8")
        print(f"----{system}系统签名参数---", sign_params)
        keySecret = self.__keySecret.encode(encoding="UTF8")
        # print("---私钥---", keySecret)
        digest = hmac.new(
            keySecret,
            sign_params,
            digestmod=hashlib.sha256).hexdigest()
        #     digestmod=hashlib.sha256).digest()
        # signature = base64.b64encode(digest)
        # signature = signature.decode()
        signature = digest
        # print("---生成的签名---", signature)

        return signature, timestamp

    def __get_sign_params(self, params: dict, method, path, timestamp):
        """获取系统签名参数"""
        body = ""
        if method in ["post", "delete", "put"]:
            body = json.dumps(params, default=str)

        elif method in ["ws", "wss"]:
            pass

        elif re.compile(r"\d+").findall(path) and not params:
            # 针对为body为空，URL是订单号的情况
            body = ""
        else:
            # get请求
            params = [f'{key}={value}' for key, value in params.items()]
            params = '&'.join(params)
            path += '?' + params

        str_to_sign = str(timestamp) + method.upper() + path + body
        return str_to_sign
