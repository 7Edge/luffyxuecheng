from rest_framework.authentication import BaseAuthentication
# from rest_framework.request import Request
# from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from pytz import timezone
import datetime

from luffyapi.models import UserToken
from django.utils.timezone import now


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        curr_datetime = datetime.datetime.now(tz=timezone('Asia/Shanghai'))
        token_obj = UserToken.objects.filter(token=token, expired__gt=curr_datetime).first()
        # print(token_obj.expired)
        # print(token_obj.expired > curr_datetime)

        if token_obj:
            return token_obj.user, token_obj.token
        else:
            raise AuthenticationFailed({
                'code': 1002,
                'error': '认证失败!'
            })
