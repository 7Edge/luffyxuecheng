#! /usr/bin/env python3
# coding:utf-8
# author:zhangjiaqi<1399622866@qq.com>
# Date:2019-01-08

"""
登录认证，登录注销
"""
import datetime
from uuid import uuid4
from datetime import timedelta
from pytz import timezone

from rest_framework import viewsets
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

from luffyapi.models import UserToken, UserInfo
from luffyapi.serializers import UserPwdModelSerializer
from luffyapi.utils.customer_response import TokenResponse

CHENGDU_TIMEZONE = timezone('Asia/Shanghai')


class AccountView(viewsets.GenericViewSet):
    """
    用于用户认证相关接口
    """
    queryset = UserInfo.objects.all()
    serializer_class = UserPwdModelSerializer

    # CORS 预检响应
    def options(self, request, *args, **kwargs):
        response_ob = Response()
        return response_ob

    # 登陆方式 帮助提示info
    def get(self, request, *args, **kwargs):
        login_prompt_info = {
            'title': 'for login to get user_token',
            'http_method': 'post',
            'Content-Type': ['支持：', 'application/json', 'form-data'],
            'content-key-value': {
                'user': 'username',
                'pwd': 'password',
            },
            'how to use token from response to pass auth': 'eg: http://127.0.0.1/mico/?token=xxxxx'
        }
        return Response(login_prompt_info)

    # 登录action
    def login(self, request, version):
        result = TokenResponse()
        result.version = version

        user = request.data.get('user')
        pwd = request.data.get('pwd')
        serializer_obj = UserPwdModelSerializer(data={'user': user, 'pwd': pwd}, many=False)

        if not serializer_obj.is_valid():
            result.code = 1001
            result.error = serializer_obj.errors
            return Response(result.dict)

        valid_data = serializer_obj.validated_data
        try:
            user_obj = self.queryset.get(**valid_data)
            new_token = str(uuid4())
            timedelta_obj = timedelta(days=1)
            # 计算获得token过期时间
            expire_datetime = datetime.datetime.now(tz=CHENGDU_TIMEZONE) + timedelta_obj
            token_obj, res = UserToken.objects.update_or_create(user=user_obj,
                                                                defaults={'token': new_token,
                                                                          'expired': expire_datetime})
        except ObjectDoesNotExist as e0:
            result.code = 1002
            result.error = "用户名或密码错误！"
        except Exception as e1:
            result.code = 1003
            result.error = "获取Token异常：" + str(e1)
        else:
            result.user_token = token_obj.token
            result.expired = token_obj.expired.strftime('%Y-%m-%d %H:%M:%S %Z')
        return Response(result.dict)


if __name__ == '__main__':
    pass
