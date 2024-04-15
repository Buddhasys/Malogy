"""
-------------------------------------------------
        Author :    albertz
        contact:    Buddha@sys.com
      File Name：   AdminInfo.py
           date：   2024/3/24
   Description :   后管相关接口操作
-------------------------------------------------
   Change Activity:
                   2024/3/24 22:06:
-------------------------------------------------
"""
import time

import requests
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from GetDictData import GetDictData as Gda


class AdminInfo:

    def __init__(self, env="test"):
        self._user = "buddha"
        self._pwd = "VSz_boP55UzUqK"
        self._verifyCode = "111111"
        self._host = {
            "test": "https://manage.xt-qa.com/api",
            "dev": "https://manage.xt-dev.com/api"
        }
        self.token = self.__sign_in(env)

    def __encrpt(self, public_key):
        """密码加密"""
        rsakey = RSA.importKey(public_key)
        cipher = Cipher_pksc1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(self._pwd.encode()))

        return cipher_text.decode()

    def __sign_in(self, env):
        """登录"""
        self._host = self._host[env]
        url_secret = self._host + "/xt-admin-uaa/publicKey"
        key_secret = Gda.get_single_value('publicKey', requests.get(url=url_secret).json())
        if not key_secret:
            return {
                "code": "40001",
                "msg": "publicKey接口异常"
            }
        public_key = '-----BEGIN PUBLIC KEY-----\n' + key_secret + '\n-----END PUBLIC KEY-----'
        pwd_secret = self.__encrpt(public_key)
        sign = {
            "userName": self._user,
            "verifyCode": self._verifyCode,
            "password": pwd_secret
        }
        url_sign = self._host + "/xt-admin-uaa/signIn"
        signed = requests.put(url=url_sign, json=sign).json()
        mfaId = Gda.get_single_value("mfaId", signed)
        if not mfaId:
            return {
                "code": "40002",
                "msg": "signIn接口异常"
            }
        header = {
            "Mfa-Id": mfaId,
            "Verify-Code": self._verifyCode
        }
        factor = self._host + "/xt-admin-uaa/multiFactor/twoFactor"
        res = requests.post(url=factor, json={}, headers=header).json()
        access_token = Gda.get_single_value("accessToken", res)
        if not access_token:
            return {
                "code": "40003",
                "msg": "twoFactor接口异常"
            }
        return access_token

    @classmethod
    def admin_deposit(cls, account, amount, coinId, obj: object):
        """后台虚增资产"""
        data = {
            "googleCode": "111111",
            "userId": account,
            "coinId": coinId,
            "remark": "",
            "amount": f"{amount}",
            "type": 1,
            "bzId": str(time.time() * 1000)[:13]
        }
        header = {
            "Token": obj.token,
            "Content-Type": "application/json",
            "Verify-Code": "111111",
        }
        url = obj._host + "/xt-fund-trans/fund/addOrSub/apply"
        res = requests.post(url=url, json=data, headers=header).json()

        return res


if __name__ == '__main__':
    token = AdminInfo().token
