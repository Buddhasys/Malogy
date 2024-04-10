"""
@author: Albertz
@license: (C) Copyright 2021-2099, Node Supply Chain Manager Corporation Limited.
@contact: Buddha@sys.com
@software: 
@file: TransAdapter.py
@time:
@desc:
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃        ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛

"""

import json, logging
from constants import Constants
from GetDictData import GetDictData as Gda
from appellant import RequestAPI, OutObj, Headers, ReplaceMsg


logger = logging.getLogger()
#### 调试用
# logging.basicConfig(level=logging.DEBUG)


class TranAdapter:
    """交易适配"""

    def __init__(self):
        self.Rem = ReplaceMsg()
        self.IO_name = None
        self._index = {
            "spot": 0,
            "future": 1,
            "wallet": 2,
            "user": 3
        }

    @classmethod
    def common_send(cls, ori_data: dict, trans_name=None, **kwargs):
        """
        所有交易经过此方法转发
        @param trans_name: 交易名称
        @param ori_data: 测试数据
        @return:
        """
        if ori_data.get("sysconf"):
            env, request, system = "prod", "rest", "api"
            adapter = ori_data.get("sysconf")
            url = adapter.get("url")
            method = adapter.get("method")
            path = adapter.get("path")
            auth = adapter.get("auth", False)
            req_data = json.loads(ori_data.get("req_data", '{}'))
        else:
            cls().IO_name = trans_name
            env = ori_data.get("env", "test").lower()
            system = ori_data.get("system", "spot").lower()
            enums = cls()._index[system]
            # 获取系统适配信息
            router = Constants().load_yaml_all()
            if isinstance(router, dict):
                return OutObj(trans_name, ori_data, router, ori_data)
            adapter = router[enums].get(trans_name, None)
            if not adapter:
                result = {
                    "code": "70001",
                    "msg": "请检查是否配置对应的信息"
                }
                return OutObj(trans_name, ori_data, result, ori_data)
            request = adapter.get("request", "").lower()
            host = router[-1].get(env, {}).get(request)
            if not host:
                result = {
                    "code": "70002",
                    "msg": "未配置该环境域名"
                }
                return OutObj(trans_name, ori_data, result, ori_data)
            adds = adapter.get("add")
            path = adapter.get("path")
            url = host.__add__(path) if path else host
            if adds:
                url, path = cls().__request_url_special(ori_data, url, path, adds)
            auth = adapter.get("auth", False)
            method = adapter.get("method", "").lower()
            message = Constants().load_yaml_all("message.yml")[enums].get(trans_name, {})
            req_data = cls().Rem.get_data(message, ori_data)
        header = Headers(system, env, auth)
        if request not in ("sws", "fws", "rest", "sapi", "fapi"):
            logger.warning(f"暂不支持处理该类型请求：{method}")
            result = {
                "code": "70003",
                "msg": f"暂不支持处理该类型请求：{method}"
            }
            return OutObj(trans_name, ori_data, result, ori_data)
        elif auth == "token":   ## 通过密码用户名拿到token
            userId = list(header.get_headers(ori_data.get('UID')).values())[0]
            headers, auth_info = header.get_signed_unify(userId,)
            if not headers:
                return OutObj(trans_name, ori_data, auth_info, ori_data)
            return cls().__get_unify_token(request, "json", url, method, req_data, headers)
        elif auth == "cookie":    ## 通过密码用户名拿到cookie
            userId = list(header.get_headers(ori_data.get('UID')).values())[0]
            headers = header.get_signed_unify(userId)
            if isinstance(headers, tuple):
                return OutObj(trans_name, ori_data, headers[1], ori_data)
            headers.update({
                "Cookie": ori_data.get("Cookie")
            })
        # 需要验签或ip需要补充
        elif auth:
            userId = list(header.get_headers(ori_data.get('UID')).values())[0]
            headers = header.get_signed_headers(userId, req_data, method, path)
            if isinstance(headers, tuple):
                return OutObj(trans_name, ori_data, headers[1], ori_data)
        else:
            userId = None
            headers = {}
        headers.update(kwargs.get("header", {}))
        logger.info(f"请求头headers：{json.dumps(headers, ensure_ascii=False, indent=4, default=str)}")
        logger.info(f"目标地址：{method or 'ws'}:{url}")
        logger.info(f"\n==========开始发送请求报文========：\n{json.dumps(req_data, ensure_ascii=False, indent=4, default=str)}")

        if method in ["post", "get", "put", "delete"]:
            res = RequestAPI().request_route("http", "json", url, method, req_data, headers=headers)
        elif method in ["ws", "wss"]:
            kwargs = cls().__ws_special_treatment(ori_data, auth)
            res = RequestAPI().request_route(method=method, url=url, req_data=req_data, auth_data=headers, system=system, **kwargs)
        else:
            res = {
                "code": "70005",
                "msg": "暂不支持该请求方式"
            }
            OutObj(trans_name, ori_data, res, ori_data)
        try:
            ori_data.update({"userId": userId})
            result = json.dumps(res.json(), ensure_ascii=False, indent=4)
        except:
            logger.warning(f"正常提取报文失败，返回的报文数据： {res}")
            result = cls().res_special_treatment(res)
        logger.info(f"\n==========返回的响应报文========：\n{result}")

        return OutObj(trans_name, req_data, result, ori_data)

    def res_special_treatment(self, res):
        """针对请求提为json，返回体是xml等不一致情况的处理"""
        try:
            data = res.text
            code = res.status_code
        except:
            data = res
            code = len(res)

        return {
            "data": data,
            "code": code,
            "message": ""
        }

    def __ws_special_treatment(self, ori_data, auth) ->dict:
        _dict = {}
        if auth:
            _dict.update({"auth": True})

        _dict.update({
            "times": ori_data.get("times", 10),
            "unsub": ori_data.get("unsub", False),
            "timeout": int(ori_data.get("timeout", 10)),
            "auth": ori_data.get("auth", False),
            "token": ori_data.get("token", ""),
        })

        return _dict

    def __request_url_special(self, ori_data, url, path, adds) -> tuple:
        if adds not in url:
            return url, path
        url.replace(adds, ori_data.get(adds))
        path.replace(adds, ori_data.get(adds))
        
        return url, path

    def __get_unify_token(self, request, sms_type, url, method, req_data, headers):
        """获取token"""
        logger.info(f"\n==========开始发送请求报文========：\n{json.dumps(req_data, ensure_ascii=False, indent=4, default=str)}")
        res = RequestAPI().request_route(request, sms_type, url, method, req_data, headers=headers)
        result = json.dumps(res.json(), ensure_ascii=False, indent=4, default=str)
        if Gda.get_single_value("code", result) == 11001 or not Gda.get_single_value("ucToken", result):
            token = Gda.get_single_value("token", result)
            req_data = {
                "token": token,
                # "googleCode": "",
                "emailCode": "123456"
            }
            url.replace("login", "loginmfa")
            res = RequestAPI().request_route(request, sms_type, url, method, req_data, headers=headers)
            result = json.dumps(res.json(), ensure_ascii=False, indent=4, default=str)

        logger.info(f"\n==========返回的响应报文========：\n{result}")

        return res



