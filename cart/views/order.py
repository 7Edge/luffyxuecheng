#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: order
# Date: 4/3/2019
"""
去支付，检验支付商品与数据库的一致性，
"""

from rest_framework.views import APIView
from rest_framework.response import Response

from luffyapi import models
from cart.authentication.auth import AccessTokenAuth
from cart.utils.response import OrderResponse


class OrderAPIView(APIView):
    authentication_classes = [AccessTokenAuth, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        result = OrderResponse()
        # 获取支付费用和使用站内币（贝里）
        beili = int(request.data.get('beili', 0))
        money = int(request.data.get('money'))

        # 验证数据合法性
        if beili < 0 or money < 0:
            result.code = 1001
            result.error = '非法金额数！'
            return Response(result.dict)
        # stock_beili = models.


if __name__ == '__main__':
    pass
