#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: customer_response
# Date: 2/21/2019


class BaseResponse(object):
    """
    用对象来替代响应字典功能
    """

    def __init__(self):
        self.code = 1000
        self.error = None

    @property
    def dict(self):
        return self.__dict__


class TokenResponse(BaseResponse):
    """
    认证返回Token响应
    """

    def __init__(self):
        super().__init__()
        self.user_token = ""
        self.expired = None


if __name__ == '__main__':
    test_response = TokenResponse()
    test_response.test = 1
    print(test_response.dict)
