#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: order
# Date: 4/3/2019
"""
去支付，检验支付商品与数据库的一致性，
"""

import uuid

from rest_framework.views import APIView
from rest_framework.response import Response

from django_redis import get_redis_connection

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import transaction
from django.shortcuts import redirect, HttpResponse
from django.urls import reverse

from luffyapi import models
from luffyapi.conf import configuration
from luffyapi.utils import alipay

from cart.authentication.auth import AccessTokenAuth
from cart.utils.response import OrderResponse
from cart.utils.price_strategies import StrategyContext, FullReductionStrategy, DiscountStrategy, DirectReduceStrategy
from cart.views.payment_center import format_hash_bytes2str
from cart.utils.china_time import china_current

redis_conn = get_redis_connection()


# 生成Alipay对象函数
def get_alipay():
    obj = alipay.AliPay(
        appid=configuration.appid,
        app_notify_url=configuration.callback_pre_url + reverse(viewname='cart:pay_notify', kwargs={'version': 'v1'}),
        # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成）
        return_url=configuration.callback_pre_url + reverse(viewname='cart:pay_result', kwargs={'version': 'v1'}),
        # 如果支付成功，重定向回到你的网站的地址。
        alipay_public_key_path=configuration.ali_pub_key_path,  # 支付宝公钥
        app_private_key_path=configuration.app_private_key_path,  # 应用私钥
        debug=True,  # 默认False, 是否使用沙箱环境
    )
    return obj


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

        course_sum = 0  # 商品最终结算价格存储
        to_day = china_current.now.date()
        # 通过循环将商品信息及券后价存储,为后续订单生成，修改优惠券状态，再
        order_detail_courses = []
        coupon_list = []

        for course_key in courses_key_iter:
            course_dict = format_hash_bytes2str(redis_conn, course_key)
            # 商品课程是否存在 & 对应的用户优惠券
            try:
                # 商品课程是否存在
                course_obj = models.DegreeCourse.objects.get(pk=course_dict.get('course_id'))
                # 商品类型是否存在（这里是周期价格策略）
                price_policy_obj = course_obj.degree_price_policy_qs.get(pk=course_dict.get('policy_id'))
                # 绑定优惠券是否存在且有效
                coupon_obj = models.CouponRecord.objects.get(pk=course_dict.get('default_coupon'), account=user,
                                                             status=0, coupon__valid_begin_date__lte=to_day,
                                                             coupon__valid_end_date__gte=to_day)

                original_price = price_policy_obj.price  # 商品类型的原价
                coupon_type = coupon_obj.coupon.coupon_type  # 商品使用的优惠券类型，根据类型进行不同算法结算

                """
                coupon_type_choices = ((0, '通用券'),
                                       (1, '折扣券'),
                                       (2, '满减券'))
                """
                # 根据不同类型，计算策略的上下文对象（策略模式应用）
                if coupon_type == 1:
                    context_strategy = StrategyContext(DiscountStrategy(coupon_obj.coupon.off_percent))
                elif coupon_type == 2:
                    context_strategy = StrategyContext(FullReductionStrategy(coupon_obj.coupon.minimum_consume,
                                                                             coupon_obj.coupon.money_equivalent_value))
                else:
                    context_strategy = StrategyContext(DirectReduceStrategy(coupon_obj.coupon.money_equivalent_value))
                # 计算出商品最终价格
                rel_price = context_strategy.cashing(original_price)

                # 分别存储遍历数据：
                coupon_list.append(coupon_obj.pk)  # 用户生成订单后，修改优惠券使用状态
                order_detail_courses.append({'course': course_obj,
                                             'original_price': original_price,
                                             'price': rel_price,
                                             'period': price_policy_obj.period})  # 用于生成订单后，生成对应的订单详情

                course_sum += rel_price

            except ObjectDoesNotExist as e:
                result.code = 1003
                result.error = '%s-%s 商品已不存在 或 优惠券已过期！' % (str(course_dict.get('name')), course_dict.get('period_str'))
            except Exception:
                raise

        # 05 计算通用优惠券，验证通用的合法性
        global_coupons_dict = format_hash_bytes2str(redis_conn, settings.USER_GLOBAL_COUPON_KEY.format(user_id=user.pk))

        try:
            global_coupon_obj = models.CouponRecord.objects.get(account=user, status=0, coupon__object_id__isnull=True,
                                                                coupon__valid_begin_date__lte=to_day,
                                                                coupon__valid_end_date__gte=to_day,
                                                                pk=global_coupons_dict.get('default_coupon')
                                                                )
            global_coupon_type = global_coupon_obj.coupon.coupon_type

            if global_coupon_type == 1:
                global_context_strategy = StrategyContext(DiscountStrategy(global_coupon_obj.coupon.off_percent))
            elif global_coupon_type == 2:
                global_context_strategy = StrategyContext(
                    FullReductionStrategy(global_coupon_obj.coupon.minimum_consume,
                                          global_coupon_obj.coupon.money_equivalent_value))
            else:
                global_context_strategy = StrategyContext(
                    DirectReduceStrategy(global_coupon_obj.coupon.money_equivalent_value))

            course_sum = global_context_strategy.cashing(course_sum)

            # 通用优惠券也加入到已使用优惠券列表
            coupon_list.append(global_coupon_obj.pk)

        except ObjectDoesNotExist as e:
            result.code = 1004
            result.error = '通用优惠券错误！'
            return Response(result.dict)

        # 06 减去贝里
        course_sum -= beili

        # 07 校验后端和前端价格
        if course_sum != 0 and course_sum != money:
            result.code = 1005
            result.error = '结算价异常'
            return Response(result.dict)

        # 08 为当前商品生成订单
        pay_type = 1  # 这里hardcode 只支持支付宝
        order_status = 1  # 默认待支付状态
        # order_status = 0 if course_sum == 0 else 1

        # 数据库修改操作进行事务
        with transaction.atomic():
            # 生成订单
            order_obj = models.Order.objects.create(payment_type=pay_type, order_number=str(uuid.uuid4()),
                                                    account=user.account,
                                                    status=order_status,
                                                    actual_amount=course_sum)
            # 生成订单详情
            order_detail_objs = []
            course_names = []
            for item in order_detail_courses:
                obj = models.OrderDetail(order=order_obj, content_object=item.get('course'),
                                         original_price=item.get('original_price'),
                                         price=item.get('price'), valid_period=item.get('period'))
                order_detail_objs.append(obj)
                course_names.append(item.get('course').name)
            order_obj.orderdetail_set.bulk_create(order_detail_objs)

            # 扣除贝里,生成贝里交易记录
            if beili > 0:
                user.account.balance -= beili
                user.account.save()

                models.TransactionRecord.objects.create(account=user.account, amount=beili, transaction_type=1,
                                                        transaction_number=uuid.uuid4(), memo="课程购买",
                                                        content_object=order_obj)

            # 优惠券更新
            models.CouponRecord.objects.filter(id__in=coupon_list).update(status=1, used_time=china_current.now,
                                                                          order=order_obj)

            # 进行支付
            if course_sum == 0:
                order_obj.status = 0
                order_obj.payment_type = 3  # 如果实际支付金额是0，那么就算做贝里支付完成的，通过查看贝里交易可以查看交易金额。
                order_obj.pay_time = china_current.now
                order_obj.save()
                result.msg = '支付完成！'
                return Response(result.dict)
            else:
                alipay_obj = get_alipay()
                query_param = alipay_obj.direct_pay(subject=';'.join(course_names), out_trade_no=order_obj.order_number,
                                                    total_amount=course_sum)
                redirect_url = alipay_obj.gateway + '?' + query_param
                result.to_url = redirect_url
                return Response(result.dict)


# 异步回调，修改订单状态视图
def async_notify(request):
    """
    回调是POST请求
    参数分为公共参数和业务参数
    参数详情列表参考：https://docs.open.alipay.com/270/105902/
    """
    infos = request.POST.dict()  # 获取请求信息已字典的形式
    sign_str = infos.pop('sign')
    pay_obj = get_alipay()
    verify_sign_status = pay_obj.verify(infos, signature=sign_str)
    if verify_sign_status:
        print('异步回调验签成功')
        # 验签成功,修改订单
        trade_status = infos.get('trade_status')
        out_trade_no = infos.get('out_trade_no')
        ali_trade_no = infos.get('trade_no')
        appid = infos.get('app_id')

        if appid != configuration.appid:
            print('appid错误！')
            return HttpResponse('failure')

        try:
            order_obj = models.Order.objects.get(order_number=out_trade_no)
        except ObjectDoesNotExist as e:
            print('订单号不存在！')
            return HttpResponse('failure')  # 订单不存在

        if order_obj.status != 1:  # 表示订单已经不是待支付状态.(订单已支付或订单取消等)
            print('订单状态已不是待支付！')
            return HttpResponse('failure')

        if order_obj.actual_amount != float(infos.get('total_amount')):
            return HttpResponse('failure')

        if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':  # 支付成功
            order_obj.payment_number = ali_trade_no
            order_obj.status = 0
            order_obj.pay_time = china_current.now
            order_obj.save()

            return HttpResponse('success')
    return HttpResponse('failure')


# 支付完成同步回调完成页面
def pay_result(request):
    data = request.GET.dict()
    print('同步回调参数:', data)
    sign = data.pop('sign')
    alipay_obj = get_alipay()
    verify_status = alipay_obj.verify(data, signature=sign)
    if verify_status:
        return HttpResponse('支付成功！')
    # return redirect(to='http://www.baidu.com')
    return HttpResponse('验签失败！异常支付！')


if __name__ == '__main__':
    pass
