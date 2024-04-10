"""
@author: Albertz
@license: (C) Copyright 2021-2099, Node Supply Chain Manager Corporation Limited.
@contact: Buddha@sys.com
@software: 
@file: ReplaceDataValue.py
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

import json
from jsonpath import jsonpath

class ReplaceDataValue:
    """替换字典中特定键的值"""


    def delete_values_by_jsonpath(self, delete_key, target_dict: dict) -> dict:
        """"
        嵌套删除json值
        @param delete_key: 要删除的key
        @param target_dict: 目标字典
        @return: 替换后的字典
        """
        if not target_dict:
            # 如果目标字典是空字典直接返回
            return target_dict
        elif isinstance(delete_key, str):
            try:
                if "[" in delete_key or "{" in delete_key or "(" in delete_key:
                    temp_data = json.loads(delete_key, encoding='utf-8')
                    delete_key = temp_data
                else:
                    delete_key = [delete_key]
            except Exception as e:
                raise Exception("replace data is not a list/dict/tuple")

        if isinstance(delete_key, list):
            for path in delete_key:
                real_paths = jsonpath(target_dict, path, result_type='IPATH')
                if real_paths:
                    for path in real_paths:
                        temp_dict = target_dict
                        for index in path[:-1]:
                            index = int(index) if isinstance(temp_dict, list) else index
                            temp_dict = temp_dict[index]
                        index = path[-1]
                        index = int(index) if isinstance(temp_dict, list) else index
                        temp_dict.pop(index)
                else:
                    raise Exception("jsonpath is not exist")

        else:
            raise Exception("data's type is error")

        return target_dict
    def addition_values_by_jsonpath(self, add_key, target_dict: dict) -> dict:
        """"
        嵌套添加json值
        @param delete_key: 要添加的key
        @param target_dict: 目标字典
        @return: 替换后的字典
        """
        if not target_dict:
            # 如果目标字典是空字典直接返回
            target_dict = {}
        if isinstance(add_key, str):
            try:
                if "[" in add_key or "{" in add_key or "(" in add_key:
                    temp_data = json.loads(add_key)
                    add_key = temp_data
                else:
                    add_key = [add_key]
            except Exception as e:
                raise Exception("replace data is not a list/dict/tuple")

        if isinstance(add_key, (list, tuple, set)):
            for key in add_key:
                target_dict.update({
                    key: ""
                })
        else:
            raise Exception("data's type is error")

        return target_dict

    def replace_json_values(self, replace_data, target_dict) -> dict:
        """
        嵌套替换json值
        @param replace_data: 要替换的字典
        @param target_dict: 目标字典
        @return: 替换后的字典
        """
        if not replace_data:
            return target_dict
        elif isinstance(replace_data, str):
            try:
                temp_data = json.loads(replace_data, encoding='utf-8')
                replace_data = temp_data
            except Exception as e:
                raise Exception("replace data is not a list/dict/tuple")

        if isinstance(replace_data, dict):
            for key in replace_data.keys():
                self.__replace_dict_value(key=key, target_dict=target_dict, replace_value=replace_data.get(key, None))
                self.__set_values_by_jsonpath(replace_data, target_dict) if "." in key else ""

        elif isinstance(replace_data, (list, tuple)):
            # 若传入的是列表或元组，则开始遍历
            for item in replace_data:
                if isinstance(item, str):
                    try:
                        temp_data = json.loads(replace_data, encoding='utf-8')
                        item = temp_data
                    except Exception as e:
                        raise Exception("The data's type is error")

                if isinstance(item, dict):
                    for key in item.keys():
                        self.__replace_dict_value(key=key, target_dict=target_dict, replace_value=item.get(key, None))
                        self.__set_values_by_jsonpath(item, target_dict) if "." in key else ""
        else:
            raise Exception("暂不支持该数据类型转换：{}".format(type(replace_data)))

        return target_dict

    def __replace_dict_value(self, key, target_dict, replace_value) -> dict:
        """
        替换指定的key为replace_data
        @param key: 要替换的key
        @param target_dict: 目标字典
        @param replace_value: 替换值
        @return:
        """
        if isinstance(target_dict, str):
            try:
                temp_data = json.loads(target_dict, encoding='utf-8')
                target_dict = temp_data
            except Exception as e:
                raise Exception("The data's type is error")

        elif not isinstance(target_dict, dict):
            raise Exception("target_dict not an dict")

        if key in target_dict.keys():
            target_dict[key] = replace_value


        else:
            for value in target_dict.values():
                if isinstance(value, dict):
                    self.__replace_dict_value(key, value, replace_value)

                elif isinstance(value, (list, tuple)):
                    self.__replace_son_target(key, value, replace_value)
                else:
                    continue

        return target_dict

    def __replace_son_target(self, key, val, replace_value):
        for _val in val:
            if isinstance(_val, dict):
                self.__replace_dict_value(key, _val, replace_value)
            elif isinstance(_val, (list, tuple)):
                # 传入的_val是列表或元组，则调用自身
                self.__replace_son_target(key, _val, replace_value)
            else:
                continue

    def __set_values_by_jsonpath(self, replace_dict: dict, target_dict: dict) -> dict:
        """
        根据jsonpath设置值
        @param replace_dict: 要替换的字典
        @param target_dict: 目标字典
        @return:
        c = {'a':1, 'b':[{'a':2},{'b':2,'a':2}], 'c':{'a':2}}
        __set_values_by_jsonpath({'b[0].a':3, 'c.a':6})
        {'a':1, 'b':[{'a':3},{'b':2,'a':2}], 'c':{'a':6}
        """
        if not target_dict:
            # 如果目标字典是空字典直接返回
            return target_dict

        for path, value in replace_dict.items():
            real_paths = jsonpath(target_dict, path, result_type='IPATH')
            if real_paths:
                for path in real_paths:
                    temp_dict = target_dict
                    for index in path[:-1]:
                        index = int(index) if isinstance(temp_dict, list) else index
                        temp_dict = temp_dict[index]
                    index = path[-1]
                    index = int(index) if isinstance(temp_dict, list) else index
                    temp_dict[index] = value

            else:
                raise Exception("jsonpath is not exist")

        return target_dict


