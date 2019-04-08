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

from django_redis import get_redis_connection

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from luffyapi import models

from cart.authentication.auth import AccessTokenAuth
from cart.utils.response import OrderResponse
from cart.utils.price_strategies import StrategyContext, FullReductionStrategy, DiscountStrategy, DirectReduceStrategy
from cart.views.payment_center import format_hash_bytes2str
from cart.utils.china_time import china_current

redis_conn = get_redis_connection()


class OrderAPIView(APIView):
    """
    支付处理
    """
    authentication_classes = [AccessTokenAuth, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        result = OrderResponse()

        # 01. 获取支付费用和使用站内币（贝里）
        beili = int(request.data.get('beili', 0))
        money = int(request.data.get('money'))

        # 02. 验证数据合法性
        if beili < 0 or money < 0:
            result.code = 1001
            result.error = '非法金额数！'
            return Response(result.dict)

        # 03. 用户剩余存量贝里数,及校验是否够用
        stock_beili = user.account.balance
        if stock_beili < beili:
            result.code = 1002
            result.error = '贝里数不够！'
            return Response(result.dict)

        # 04 计算用户支付中心的商品用券后价格,及校验商品和优惠券可用性
        courses_key_iter = redis_conn.scan_iter(match=settings.PAYMENT_CENTER_KEY.format(user_id=user.pk,
                                                                                         course_id='*'))

        course_sum = 0

        for course_key in courses_key_iter:
            course_dict = format_hash_bytes2str(redis_conn, course_key)

            # 商品课程是否存在 & 对应的用户优惠券
            try:
                course_obj = models.DegreeCourse.objects.get(pk=course_dict.get('course_id'))

                price_policy_obj = course_obj.degree_price_policy_qs.get(pk=course_dict.get('policy_id'))

                to_day = china_current.now.date()
                coupon_obj = models.CouponRecord.objects.get(pk=course_dict.get('default_coupon'), account=user,
                                                             status=0, coupon__valid_begin_date__lte=to_day,
                                                             coupon__valid_end_date__gte=to_day)
                original_price = price_policy_obj.price
                coupon_type = coupon_obj.coupon.coupon_type

                """
                coupon_type_choices = ((0, '通用券'),
                                       (1, '折扣券'),
                                       (2, '满减券'))
                """
                if coupon_type == 1:
                    context_strategy = StrategyContext(DiscountStrategy(coupon_obj.coupon.off_percent))
                elif coupon_type == 2:
                    context_strategy = StrategyContext(FullReductionStrategy(coupon_obj.coupon.minimum_consume,
                                                                             coupon_obj.coupon.money_equivalent_value))
                else:
                    context_strategy = StrategyContext(DirectReduceStrategy(coupon_obj.coupon.money_equivalent_value))

                course_sum += context_strategy.cashing(original_price)

            except ObjectDoesNotExist as e:
                result.code = 1003
                result.error = '%s-%s 商品已不存在 或 优惠券已过期！' % (str(course_dict.get('name')), course_dict.get('period_str'))
            except Exception:
                raise

        # 05 计算通用优惠券，验证通用的合法性


if __name__ == '__main__':
    pass
