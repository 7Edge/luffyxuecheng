from django.test import TestCase

import alipay

from django.forms.models import model_to_dict
# Create your tests here.

from django.forms import Form

from rest_framework.mixins import ListModelMixin

from rest_framework.generics import GenericAPIView

from rest_framework.relations import HyperlinkedIdentityField

from django.urls import reverse

from django.urls import include

from  django.middleware.csrf import CsrfViewMiddleware


# 0.1 视图view
from rest_framework import views  # APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets

# 02. 路由router
from rest_framework import routers

# 03. 解析parser
from rest_framework import parsers

# 04. 内容协商negotiation
from rest_framework import negotiation

# 05. 版本version
from rest_framework import versioning

# 06. 渲染器render
from rest_framework import renderers

# 07. 认证authentication
from rest_framework import authentication

# 08. 权限permission
from rest_framework import permissions

# 09. 频率控流throttling
from rest_framework import throttling

# 10. 序列化serializer
from rest_framework import serializers
from rest_framework import relations
from rest_framework import fields

# 11. 分页pagination
from rest_framework import pagination


# 12. 请求Request
from rest_framework import request

# 13. 响应Response
from rest_framework import response
