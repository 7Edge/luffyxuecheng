#! /usr/bin/env python3
# coding:utf-8
# author:zhangjiaqi<1399622866@qq.com>
# Date:2019-01-16
import time

from rest_framework.views import APIView
from rest_framework.response import Response

from luffyapi.auth.token_auth import TokenAuthentication


class MicroView(APIView):
    authentication_classes = [TokenAuthentication, ]

    # 对深科技视图进行缓存
    def get(self, request, *args, **kwargs):
        # 获取深科技信息列表
        return Response({'code': 1000,
                         'data': '深科技',
                         'time': time.time()})
