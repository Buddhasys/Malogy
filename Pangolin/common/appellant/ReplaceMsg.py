"""
-------------------------------------------------
        Author :    albertz.yang
        contact:    albertz.yang@poloniex.com
      File Name：   ReplaceMsg
           date：   2021/12/28 8:26 上午
   Description :
-------------------------------------------------
   Change Activity:
                   2021/12/28:
-------------------------------------------------
"""
import json, logging, time
from ReplaceDataValue import ReplaceDataValue as Rep

logger = logging.getLogger()


class ReplaceMsg:
    """支付交易"""

    def __init__(self):
        self.Rep = Rep()

    def get_data(self, origin_data, test_data):
        """获取测试数据"""
        replace_data = {
            "clOrdId": str(time.strftime('%m%d%H%M%S',
                            time.localtime())+str(time.time()).split('.')[-1])
        }
        # 正常场景
        if isinstance(test_data, dict):
            replace_data.update(test_data)

        elif not test_data:
            logger.warning(f"传入的测试数据为空")

        else:
            try:
                replace_data.update(json.loads(test_data, encoding='utf-8'))
            except:
                logger.warning(f"传入的测试数据格式不正确： {test_data}")

        # 删除模板键值
        if "del" in test_data.keys():
            origin_data = self.Rep.delete_values_by_jsonpath(test_data.get("del"), origin_data)
        # 添加模板键值
        if "add" in test_data.keys():
            origin_data = self.Rep.addition_values_by_jsonpath(test_data.get("add"), origin_data)

        logger.info(f"开始替换报文:\n{json.dumps(replace_data,ensure_ascii=False,indent=4, default=str)}")
        return self.Rep.replace_json_values(replace_data, origin_data)
