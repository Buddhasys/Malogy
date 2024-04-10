"""
@author: Albertz
@license: (C) Copyright 2021-2099, Node Supply Chain Manager Corporation Limited.
@contact: Buddha@sys.com
@software:
@file: ExcelDataProcess.py
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
import logging
import os
import pandas as pd
from ResValidator import ResValidator as sdv


class ExcelDataProcess:
    """获取数据"""

    @classmethod
    def get_excel(cls, data_path, trans_scene="Sheet1"):
        """
        获取表格文件
            @param trans_scene: 交易名称
            @return: 数据字典
        """
        # 读取表格数据
        req_data = []
        origin_dict = dict()  # 存储处理后的数据
        excel_data = pd.ExcelFile(data_path)
        if trans_scene in excel_data.sheet_names:
            sheet_data = excel_data.parse(sheet_name=trans_scene).fillna('')
            # usecols要么全字符要么全数字，数字时表示读取的列，字符表示列名,fillna将所有为空的值（NaN）替换成空字符
        else:
            raise ValueError("表格中找不到该交易数据")
        # 获取表头，返回的是list
        sheet_header = sheet_data.columns.tolist()
        # sheet_data.index得到的是RangIndex对象，通过values方法获取对象里面的值,这个值的类型是ndarray
        # 不管是matrix对象还是ndarray对象都可以用object.tolist()方法转换成列表
        for index in sheet_data.index.values.tolist():
            # 获取每行数据
            sheet_line = sheet_data.loc[index].values   # 读取每行数据
            try:
                # 获取字段的最大长度
                _dict = dict(zip(sheet_header, sheet_line))
                origin_dict[index] = _dict
                url = _dict.get("URL", "") or _dict.get("请求地址", "")
                temp = {
                    "req_data": _dict.get("请求参数") or _dict.get("输入参数"),
                    "sysconf": {
                        "url": url,
                        "url_path": f'/api/{url.split("api/", 1)[-1]}',
                        "req_way": _dict.get("请求方式"),
                        "auth": _dict.get("私有接口") or _dict.get("AUTH"),
                    },
                    "expect": _dict.get("预期结果", ""),
                    "apiname": _dict.get("接口名称", ""),
                    "filename": data_path.split("/")[-1].split(".")[0]
                }
                req_data.append(temp)
            except Exception as e:
                logging.warning(e)
                break

        return req_data, origin_dict

    @classmethod
    def write_excel(cls, datas, write_path):
        """写表"""
        if datas.data["expect"] and isinstance(datas.data["expect"], dict):
            expect = datas.data["expect"]
        elif datas.data["expect"] and isinstance(datas.data["expect"], str):
            expect = eval(datas.data["expect"])
        else:
            expect = {}
        valid = sdv.verify_trading_datas(datas.response, expect)
        xlsx_data = {
            "接口名称": [datas.data["apiname"]],
            "请求地址": [datas.res.url],
            "请求方式": [datas.res.request.method],
            "状态码": [datas.res.status_code],
            "请求参数": [json.dumps(datas.request, ensure_ascii=False, indent=4)],
            "实际结果": [json.dumps(datas.response, ensure_ascii=False, indent=4)],
            "预期结果": [json.dumps(expect, ensure_ascii=False, indent=4)],
            "断言结果": [valid[0]],
            "校验详情": [valid[1]],
        }

        if not os.path.exists(write_path):
            df = pd.DataFrame(xlsx_data)
            df.to_excel(write_path, index=False)
        else:
            ori = cls.get_excel(write_path)[1]
            for _dict in ori.values():
                for key, val in xlsx_data.items():
                    val.append(_dict[key])
            df = pd.DataFrame(xlsx_data)
            df.to_excel(write_path, index=False)





