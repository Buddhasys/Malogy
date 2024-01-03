"""
-------------------------------------------------
        Author :    albertz.king
        contact:    albertz.king@bitget.com
      File Name：   OrderBooks.py
           date：   2023/12/1
   Description :  铺单
-------------------------------------------------
   Change Activity:
                   2023/12/01 22:06:
-------------------------------------------------
"""
import math, time
import threading
from decimal import Decimal
from threading import Thread
from common.constants import Constants
from common.GetDictData import GetDictData as Gda
from common.TransAdapter import TranAdapter as Router


class OrderBooks:

    _req_data = None

    @classmethod
    def drape_order_book(cls, env=None, system=None, symbol=None,
                         times=1, quantity=0, notch=10, **kwargs):
        """
            铺单
        :param env: 环境
        :param system: 交易类型
        :param symbol: 币对
        :param times: 铺单次数
        :param quantity: 每档委托数量
        :param notch: 买卖方各档位
        :return:
        """
        cls._req_data = {
            "env": env,
            "system": system,
        }
        curr_price = cls().__get_trade_price(symbol)
        if isinstance(curr_price, dict):
            return curr_price
        config = cls().__get_symbol_price_scale(system, symbol)
        if not isinstance(config, dict):
            return {
                "code": "20002",
                "data": [],
                "msg": config
            }
        else:
            min_amount = config["min_amount"]
            quantity_scale = config["quantity_scale"]
            quantity = math.ceil(Decimal(str(quantity)) / quantity_scale) * quantity_scale
            min_count = math.ceil(min_amount / curr_price / quantity_scale) * quantity_scale
            quantity = Decimal(str(max(min_count, quantity))) / quantity_scale
        while times:
            buy = threading.Thread(target=cls().__place_order, args=[symbol, curr_price, config["price_scale"], quantity, notch, "buy"])
            sell = threading.Thread(target=cls().__place_order, args=[symbol, curr_price, config["price_scale"], quantity, notch, "sell"])
            buy.start()
            sell.start()
            times -= 1
        return {
            "code": "00000",
            "msg": "铺单成功",
        }

    def __place_order(self, symbol, curr_price, scale, quantity, notch, direction):

        while notch:
            self._req_data.update({
                "symbol": symbol,
                "side": direction,
                "price": str(curr_price),
                "orderQty": str(quantity),
                "positionSide": "long" if direction=="buy" else "short",
            })
            res = Router.common_send(self._req_data, "place")
            assert Gda.get_single_value('code', res.response) == "0", \
                Gda.get_single_value('message', res.response)
            if direction == "buy":
                curr_price -= scale
            else:
                curr_price += scale
            notch -= 1

    def __get_trade_price(self, symbol):
        """获取最新成交价"""
        self._req_data.update({
            "symbol": symbol,
        })
        res = Router.common_send(self._req_data, "ticker", header={
            "x-locale": "zh-CN",
            "source": "api"
        })
        if Gda.get_single_value("code", res.response) != "0":
            return res.response
        curr_price = Decimal(str(Gda.get_single_value("lastPrice", res.response)))

        return curr_price

    def __get_symbol_price_scale(self, system, symbol):
        """获取币对价格精度和最小挂单数量"""
        self._req_data.update({
            "symbol": symbol,
        })
        res = Router.common_send(self._req_data, "symbol")
        res = res.response
        if Gda.get_single_value("code", res) != "0":
            return Gda.get_single_value("msg", res)
        price_scale = Decimal(str(Gda.get_single_value("quotePrecision", res)
                                  if system == "spot" else
                                  Gda.get_single_value("tickSize", res)))
        min_amount = Decimal(str(Gda.get_single_value("minTradeUSDT", res)
                                   if system == "spot" else 5))
        quantity_scale = Decimal(str(Gda.get_single_value("basePrecision", res)
                                     if system == "spot" else
                                     Gda.get_single_value("ctVal", res)))

        return {
            "min_amount": min_amount,
            "price_scale": price_scale,
            "quantity_scale": quantity_scale,
        }
