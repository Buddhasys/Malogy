"""
@author: Albertz
@license: (C) Copyright 2021-2099, Node Supply Chain Manager Corporation Limited.
@contact: Buddha@sys.com
@software: 
@file: GetDictData.py
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

import json, random, re
from jsonpath import jsonpath


class GetDictData:
    """获取字典中的键值"""
    def __init__(self):
        self.filter_dict = {}

    @classmethod
    def get_single_value(cls, key, test_data):
        """
        根据键值，获取测试数据中的value
        @param key: 键值
        @param test_data: 测试的字典
        @return:
        """
        try:
            temp_dict = cls().__get_key_value(key, test_data)[0]
            temp_list = [v for v in temp_dict.values()]

            if len(temp_list) > 1:
                for item in temp_list:
                    if item:
                        return item
                    elif item == 0:
                        return item
            return temp_list[0]
        except:
            return

    @classmethod
    def get_multiple_value(cls, key, test_data) -> list:
        """
        根据键值，获取测试数据中的value
        @param key: 键值
        @param test_data: 测试的字典
        @return:
        """
        try:
            temp_dict = cls().__get_key_value(key, test_data)[0]
            return [v for v in temp_dict.values()]
        except:
            return []

    def __get_key_value(self, key, test_dict):
        """
            对传入的Json数据进行校验，是否满足格式要求，满足则传入获取目标值
            @param key: 键值
            @param test_dict: 测试数据
            @return: 目标值字典
        """
        filter_dict, temp_key = {}, key
        if isinstance(test_dict, (list,tuple)):
            test_dict = {"data": test_dict}
        if not isinstance(test_dict, dict):
            err_msg = "传入的数据不是字典：{}".format(test_dict)

            if isinstance(test_dict, str):
                try:
                    temp_dict = json.loads(test_dict)
                    test_dict = temp_dict
                except Exception as e:
                    raise Exception(err_msg)

            else:
                raise Exception(err_msg)

        if isinstance(key, str):
            try:
                temp_key = json.loads(test_dict, encoding="utf-8")

            except Exception as e:
                temp_key = [key]

        if not isinstance(temp_key, (list, tuple)):
            return filter_dict

        return [self.__get_target_value(_key, test_dict, filter_dict) for _key in temp_key]


    def __get_target_value(self, key, test_dict, filter_dict) -> dict:
        """
        通过key获取字典value，支持嵌套
        @param key: 目标key值
        @param test_dict: 已被格式化成字典的数据
        @param filter_dict: 用于存储获取的数据字典
        @return: 获取到的数据
        """
        if not isinstance(test_dict, dict) or not isinstance(filter_dict, dict):
            raise Exception("传入的数据不是字典类型：{}".format(test_dict))

        if key in test_dict.keys():

            new_key = "_".join([key, "temp", str(random.randint(0, 100))]) \
                if key in filter_dict.keys() else key
            filter_dict[new_key] = test_dict.get(key, "")

        # 通过'.'判断，key是不是通过jsonpath表达式传入的
        elif "." in key:
            _key = key
            if not isinstance(_key, list):
                _key = [key]
            for path in _key:

                values = jsonpath(test_dict, path)
                if values:
                    real_paths = jsonpath(test_dict, path, result_type='IPATH')
                    filter_dict[real_paths[0][-1]] = values[0]

                    return filter_dict
                else:
                    continue

        for value in test_dict.values():
            temp_value = value
            if isinstance(value, str):

                try:
                    temp_value = json.loads(value)
                except:
                    temp_value = value
            if isinstance(temp_value, dict):
                self.__get_target_value(key, temp_value, filter_dict)

            elif isinstance(temp_value, (list, tuple)):
                self.__get_value(key, temp_value, filter_dict)
        self.filter_dict.update(filter_dict) if filter_dict else None
        return self.filter_dict

    def __get_value(self, key, val, filter_dict):
        """通过key获取嵌套字典的value子方法"""
        if not val:
            return
        for _val in val:
            if isinstance(_val, dict):
                self.__get_target_value(key, _val, filter_dict)
            elif isinstance(_val, (list, tuple)):
                self.__get_value(key, _val, filter_dict)
            elif isinstance(_val, str) and re.search(r"^\[.*\]$|^\{.*\}$|^\(.*\)$", _val):
                self.__get_key_value(key, _val)
            else:
                pass
