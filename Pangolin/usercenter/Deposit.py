"""
-------------------------------------------------
        Author :    albertz
        contact:    Buddha@sys.com
      File Name：   Deposit.py
           date：   2023/12/2
   Description :  虚拟币充值
-------------------------------------------------
   Change Activity:
                   2023/12/02 11:30:
-------------------------------------------------
"""
from AdminInfo import AdminInfo
from GetDictData import GetDictData as Gda
from common.TransAdapter import TranAdapter as Router


class Deposit:
    
    @classmethod
    def admin_deposit(cls, env="test", amount=1000, coin="USDT"):
        """
                后台充值
                :param env: 环境
                :param amount: 充值数量
                :param token: 充值币种
                :return: dict
        """
        obj = AdminInfo(env)
        if isinstance(obj.token, dict):
            return obj.token
        res = obj.admin_deposit(amount, coin, obj)


    def inter_withdraw(self, env="test", amount=1000, token="USDT",
                 chain="Ethereum", address=None, memo=""):
        """
                内部业务充提
                :param env: 环境
                :param amount: 充值数量
                :param token: 充值币种
                :param account: 充值账户——现货、杠杆
                :return: dict
        """
        pass

    def withdraw(self, env="test", amount=1000, token="USDT",
                 chain="Ethereum", address=None, memo=""):
        """
                链上业务充提
                :param env: 环境
                :param amount: 充值数量
                :param token: 充值币种
                :return: dict
        """
        data = {
            "env": env,
            "system": "wallet",
            "currency": token,
            "amount": amount,
            "chain": chain,
            "address": address,
            "memo": memo,
        }
        res = Router.common_send(ori_data=data, trans_name="withdraw")
        code = Gda.get_single_value("mc", res.response)
        if code == "SUCCESS":
            return {
                "code": "20000",
                "msg": f"成功充值：{amount}{token}"
            }
        return {
            "code": code,
            "msg": "充值失败"
        }


if __name__ == '__main__':
    print(Deposit().admin_deposit())

