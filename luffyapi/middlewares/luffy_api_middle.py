#! /usr/bin/env python3
# coding:utf-8
# author:zhangjiaqi<1399622866@qq.com>
# Date:2018-12-24

"""
luffy api 中间件
"""
from django.utils.deprecation import MiddlewareMixin
from collections import Iterable
from django.http import HttpResponse

from ..conf.configuration import allow_sites


class CorsMiddleWare(MiddlewareMixin):
    @staticmethod
    def get_cors_header(request):
        if isinstance(allow_sites, str) or not isinstance(allow_sites, Iterable):
            assert allow_sites == '*', Exception('Access-Control-Allow-Origin 需要一个可迭代或者*')
        for site in allow_sites:
            # scheme, host = site.split('://', maxsplit=1)
            # print(scheme, host, request.META.get('HTTP_ORIGIN'))
            if site == request.META.get('HTTP_ORIGIN'):
                return site

    def process_request(self, request):
        """
        对于请求方式是options的直接拦截掉，然后让process_response来响应处理，返回给用户
        :param request:
        :return:
        """
        if request.method == 'OPTIONS':  # 直接在这里将options请求截断,并添加上响应头，如果要单个资源进行option的话再考虑。
            response = HttpResponse()
            response['Access-Control-Allow-Methods'] = 'PUT'
            response['Access-Control-Allow-Headers'] = "Content-Type,"
            return response

    def process_response(self, request, response):
        """

        目前对所有app的响应都加了该头
        :param request:
        :param response:
        :return:
        """
        allow_site = self.get_cors_header(request) or ''
        response['Access-Control-Allow-Origin'] = allow_site  # 注意对全部都请求都必须添加上，就算是options预检查的也要添加，
        # 因为浏览器对与检查的响应首先也是检查这个请求头，在进行请求的检查，也就是所有包括options的响应都是要有Origin的。
        return response


if __name__ == '__main__':
    pass
