"""
-------------------------------------------------
        Author :    albertz king
        contact:    albertz@gmail.com
      File Name：   ResValidator.py
           date：   2023/05/26 6:33 下午
   Description :
-------------------------------------------------
   Change Activity:
                   2023/05/26:
-------------------------------------------------
"""
from copy import deepcopy
from json_tools import diff
from DataVerify import DataVerify
from GetDictData import GetDictData as Gda


class ResValidator:

    @classmethod
    def verify_trading_datas(cls, actual, expect):
        """校验数据"""
        _actual, _expect = deepcopy(actual), deepcopy(expect)
        if not expect:
            return False, "未写预期值"
        actual_value = Gda.get_single_value("data", actual)
        expect_value = Gda.get_single_value("data", expect)
        if not actual_value or not expect_value:
            return Gda.get_single_value("code", actual) == Gda.get_single_value("code", expect), "data为空, 仅校验code"
        elif (isinstance(expect_value, list) or isinstance(actual_value, list)) \
                and ("[" in str(expect_value) or "]" in str(actual_value)) and "[]" in str(actual_value):
            return cls().replica_json_compare(actual, expect)
        else:
            del _actual["data"], _expect["data"]
            actual_value.update(_actual)
            expect_value.update(_expect)
        _compare = DataVerify()._compare_dict_data(actual_value, expect_value)
        if not _compare[0] and not _compare[1]:
            return True, "校验成功"
        err = [_err[0] for _err in _compare[0]] if _compare[0] else []
        ign = [_err[0] for _err in _compare[1]] if _compare[1] else []

        return False, f"数据不一致的key：{err} \n; 实际不存在的key：{ign}"

    def replica_json_compare(self, actual, expect):
        """字典中嵌套列表进行校验"""
        _diff = diff(actual, expect)
        if not _diff:
            return True, "校验成功"
        elif isinstance(_diff, dict):
            _diff = [_diff]
        else:
            return None, "不支持校验"
        _error = []
        for item in _diff:
            _error.append(item.get('add'))
            _error.append(item.get('remove'))
            _error.append(item.get('replace'))
        res = [i for i in _error if not i]

        return [False, f"数据不一致的key：{res}"] if res else [True, "校验成功"]




