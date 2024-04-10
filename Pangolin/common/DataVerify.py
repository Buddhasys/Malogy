"""
@author: Albertz
@license: (C) Copyright 2021-2099, Node Supply Chain Manager Corporation Limited.
@contact: Buddha@sys.com
@software: 
@file: DataVerify
@time:
@desc:
              幸运女神保佑        永无BUG
 *
 *                      .::::.
 *                    .::::::::.
 *                   :::::::::::
 *                ..:::::::::::'
 *             '::::::::::::'
 *               .::::::::::
 *          '::::::::::::::..
 *               ..::::::::::::.
 *             ``::::::::::::::::
 *              ::::``:::::::::'        .:::.
 *             ::::'   ':::::'       .::::::::.
 *           .::::'      ::::     .:::::::'::::.
 *          .:::'       :::::  .:::::::::' ':::::.
 *         .::'        :::::.:::::::::'      ':::::.
 *        .::'         ::::::::::::::'         ``::::.
 *    ...:::           ::::::::::::'              ``::.
 *   ```` ':.          ':::::::::'                  ::::..
 *                      '.:::::'                    ':'````..
"""

import logging as logger
from decimal import Decimal


class DataVerify:
    """数据校验"""

    def __init__(self):
        self.__succ = []
        self.__err = []
        self.__ign = []
        self.__ori = []
        self.__flag = None
        self.__ori_flag = False


    @classmethod
    def data_verify(cls, actual_value: dict, expect_value: dict,
                    desc_info: dict=None, origin_value: dict=None, **kwargs):
        """
        数据进行比对校验，返回比对后的列表
        @param actual_value: 实际值
        @param expect_value: 期望值
        @param desc_info:  字段中文描述
        @param origin_value: 初始值
        @return:
        """

        return cls()._compare_dict_data(actual_value, expect_value, desc_info, origin_value)

    def _compare_dict_data(self, actual_value, expect_value, desc_info=None, origin_value=None):
        """
        比对字段数据
        @param actual_value:
        @param expect_value:
        @param desc_info:
        @param origin_value:
        @return:
        """
        if origin_value:
            self.__ori_flag = True

        for key in expect_value.keys():
            #### 兼容key是数字的情况 ####

            try:
                if key in actual_value.keys():
                    self.__campare_value(key, actual_value[key], expect_value[key]) \
                        if not self.__ori_flag else \
                        self.__campare_value(key, actual_value[key], expect_value[key], origin_value[key])
                ######  兼容期望值是数字的情况  ######
                elif isinstance(key, (int, float, Decimal)):
                    try:
                        crux = key
                        for cru in actual_value.keys():
                            if Decimal(str(cru)) == Decimal(str(key)):
                                crux = cru
                                break
                        self.__campare_value(key, actual_value[crux], expect_value[key]) \
                            if not self.__ori_flag else \
                            self.__campare_value(key, actual_value[crux], expect_value[key], origin_value[key])
                    except:
                        pass
                elif self.__ori_flag:
                    self.__ign.append([key, [origin_value[key], expect_value[key], actual_value.get(key), 'ignore']])
                else:
                    self.__ign.append([key, [expect_value[key], actual_value.get(key), 'ignore']])
            except Exception as e:
                if self.__ori_flag:
                    self.__ign.append([key, [origin_value[key], expect_value[key], actual_value.get(key), 'ignore']])
                else:
                    self.__ign.append([key, [expect_value[key], actual_value.get(key), 'ignore']])

        return self.__err, self.__ign, self.__succ

    def __campare_value(self, key, real_val, expect_val, origin_val=None):
        """
        两个值比较
        @param real_val:
        @param expect_val:
        @return:
        """
        if not real_val and not expect_val:
            self.__flag = 'success'
            self.__succ.append([key, [expect_val, real_val, self.__flag]]) \
                if not self.__ori_flag else \
                self.__succ.append([key, [origin_val, expect_val, real_val, self.__flag]])

        elif isinstance(real_val, type(expect_val)):
            if real_val == expect_val:
                self.__flag = 'success'
                self.__succ.append([key, [expect_val, real_val, self.__flag]]) \
                    if not self.__ori_flag else \
                    self.__succ.append([key, [origin_val, expect_val, real_val, self.__flag]])
            else:
                self.__flag = 'fail'
                self.__err.append([key, [expect_val, real_val, self.__flag]]) \
                    if not self.__ori_flag else \
                    self.__err.append([key, [origin_val, expect_val, real_val, self.__flag]])

        elif not isinstance(real_val, type(expect_val)):
            try:
                real_val = type(expect_val)(real_val)
            except:
                try:
                    expect_val = type(real_val)(expect_val)
                except:
                    pass
            if isinstance(expect_val,(int, Decimal, float)):
                try:
                    real_val = Decimal(str(real_val))
                    expect_val = Decimal(str(expect_val))
                except:
                    pass
            if real_val == expect_val:
                self.__flag = 'success'
                self.__succ.append([key, [expect_val, real_val, self.__flag]]) \
                    if not self.__ori_flag else \
                    self.__succ.append([key, [origin_val, expect_val, real_val, self.__flag]])
            else:
                self.__flag = 'fail'
                self.__err.append([key, [expect_val, real_val, self.__flag]]) \
                    if not self.__ori_flag else \
                    self.__err.append([key, [origin_val, expect_val, real_val, self.__flag]])
