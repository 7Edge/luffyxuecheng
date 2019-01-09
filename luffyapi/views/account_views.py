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
# from rest_framework.decorators import action

from luffyapi.models import UserToken, UserInfo
from luffyapi.serializers import UserPwdModelSerializer


CHENGDU_TIMEZONE = timezone('Asia/Shanghai')


class AccountView(viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserPwdModelSerializer

    # CORS 预检响应
    def options(self, request, *args, **kwargs):
        response_ob = Response()
        response_ob['Access-Control-Allow-Methods'] = ''
        response_ob['Access-Control-Allow-Headers'] = "Content-Type,"
        return response_ob

    # 登录action
    def login(self, request, version):
        result = {
            "code": 1000,
            "version": version,
        }
        user = request.data.get('user')
        pwd = request.data.get('pwd')
        serializer_obj = UserPwdModelSerializer(data={'user': user, 'pwd': pwd}, many=False)
        if serializer_obj.is_valid():
            valid_data = serializer_obj.validated_data
            user_obj = self.queryset.filter(**valid_data).first()
            if user_obj:
                new_token = str(uuid4())
                timedelta_obj = timedelta(days=1)
                # expire_datetime = datetime.datetime.now() + timedelta_obj
                expire_datetime = datetime.datetime.now(tz=CHENGDU_TIMEZONE) + timedelta_obj
                try:
                    token_obj, res = UserToken.objects.update_or_create(user=user_obj,
                                                                        defaults={'token': new_token,
                                                                                  'expired': expire_datetime})
                    result['user_token'] = token_obj.token
                    result['expired'] = token_obj.expired.strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    result['code'] = 1003
                    result['error'] = "获取Token异常：" + str(e)
            else:
                result['code'] = 1002
                result['error'] = "用户名或密码错误！"
        else:
            result['code'] = 1001
            result['error'] = serializer_obj.errors
        return Response(result)


if __name__ == '__main__':
    pass
