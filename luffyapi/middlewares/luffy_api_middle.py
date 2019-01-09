#! /usr/bin/env python3
# coding:utf-8
# author:zhangjiaqi<1399622866@qq.com>
# Date:2018-12-24

"""
luffy api 中间件
"""
from django.utils.deprecation import MiddlewareMixin
from collections import Iterable

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

    def process_response(self, request, response):
        """
        目前对所有app的响应都加了该头
        :param request:
        :param response:
        :return:
        """
        allow_site = self.get_cors_header(request) or ''
        response['Access-Control-Allow-Origin'] = allow_site
        return response


if __name__ == '__main__':
    pass
