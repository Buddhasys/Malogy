"""
@author: Albertz
@license: (C) Copyright 2021-2099, Node Supply Chain Manager Corporation Limited.
@contact: Buddha@sys.com
@software: 
@file: HttpRequest
@time:
@desc:  支持HTTP或HTTPS请求的发送和处理
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

import requests


class HttpRequest:
    """http/https请求处理"""

    def request(self, url, req_way, **kwargs):
        """
        http请求
        @param url: 请求地址
        @param req_data: 请求数据
        @param kwargs: 预留
        @return:
        """
        # 需要进行的数据处理
        if "json" in kwargs.keys() and not kwargs.get("json"):
            del kwargs["json"]
        return self.__getattribute__(req_way)(url, **kwargs)


    def post(self, url, **kwargs):
        """post请求"""

        return requests.post(url, **kwargs)

    def get(self, url, **kwargs):
        """get请求"""

        return requests.get(url, **kwargs)

    def delete(self, url, **kwargs):
        """delete请求"""
        return requests.delete(url, **kwargs)

    def put(self, url, **kwargs):
        """post请求"""
        return requests.put(url, **kwargs)





