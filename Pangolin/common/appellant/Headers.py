"""
-------------------------------------------------
        Author :    albertz
        contact:    Buddha@sys.com
      File Name：   Headers
           date：   2021/12/28 12:11 下午
   Description :
-------------------------------------------------
   Change Activity:
                   2021/12/28:
-------------------------------------------------
"""
import random
import logging
from enum import Enum, unique
from constants import Constants
from .Signature import Signature

logger = logging.getLogger()

@unique
class Env(Enum):
    dev = 0
    test = 1
    prod = 2


class Headers:

    def __init__(self, sys, env, auth):
        self.__env = env
        self.__sys = sys
        self.__auth = auth
        self.__box = Constants().load_yaml_all("lockbox.yml")
        
    def get_headers(self, userId=None) -> dict:
        """定制请求头"""
        headers = {  #### 没有默认给dev环境ID ####
            "XXXX": str(userId) if userId else 4859222483
        }
        logger.info(f"正在操作的用户是：\n{headers}")
        return headers

    def get_signed_headers(self, userId, req_data, req_way, urladd):
        auth_info = self.__box[getattr(Env, self.__env).value].get(userId)
        if not auth_info:
            return None, {
                "code": "70004",
                "msg": "验签失败"
            }
        else:
            headers = {
                "xt-validate-appkey": auth_info["apikey"],
                "xt-validate-timestamp": 0,
                "xt-validate-algorithms": "HmacSHA256",
                "xt-validate-recvwindow": "60000"
            }
        sign, timestamp = Signature(**auth_info).create_sign(params=req_data, method=req_way.lower(),
                                                             path=urladd, system=self.__sys, headers=headers)
        if self.__sys in ["api", "spot", "future", "wallet", "user"]:
            headers.update({
                "xt-validate-signature": sign
            })

        else:
            headers = {
                "PF-API-SIGN": sign,
                "PF-API-TIMESTAMP": str(timestamp),
                "PF-API-KEY": auth_info["apikey"],
                "PF-API-PASSPHRASE": auth_info["passphrase"]
            }
        logger.info(f"成功获取【{self.__sys}】系统请求头")
        return headers

    def get_signed_unify(self, userId):
        auth_info = self.__box[getattr(Env, self.__env).value].get(f"{userId}T")
        if self.__auth in ["token"]:
            headers = {
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "Accept-Language": "zh-CN"
            }
            return headers, auth_info

        elif self.__auth in ["cookie"]:
            headers = {
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "Accept-Language": "zh-CN"
            }
            return headers

        elif not auth_info:
            return None, {
                "code": "70004",
                "msg": "验签失败"
            }

