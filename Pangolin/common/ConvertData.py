"""
@author: Albertz
@license: (C) Copyright 2021-2099, Node Supply Chain Manager Corporation Limited.
@contact: Buddha@sys.com
@software: 
@file: ConvertData
@time:
@desc:  数据转换
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

import xmltodict, json
from xml.dom import minidom



class ConvertData:
    """数据转换处理"""

    def json_to_xml(self, convert_data):
        """
        将json格式数据转换成xml格式数据返回
        @param convert_data: 待转换数据
        @return:
        """
        return xmltodict.unparse(convert_data, encoding='utf-8')

    def xml_to_dict(self, convert_data):
        """
        将xml格式数据转换成dict格式数据返回
        @param convert_data: 待转换数据
        @return:
        """
        return xmltodict.parse(convert_data, encoding='utf-8')

    def json_format(self, json_data: dict):
        """
        json数据格式化
        @param json_data:
        @return:
        """
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        return json.dumps(json_data, ensure_ascii=False, indent=4)

    def xml_format(self, xml_data):
        """
        xml数据格式化
        @param xml_data:
        @return:
        """
        xml_obj = minidom.parseString(xml_data)
        xml_pretty_str = xml_obj.toprettyxml()

        return xml_pretty_str



