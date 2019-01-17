"""luffyuecheng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from rest_framework import routers

from luffyapi.views import courses_views
from luffyapi.views import account_views
from luffyapi.views import micro_news_views

luffyapi_router = routers.SimpleRouter()
luffyapi_router.register(r'course', courses_views.CoursesModelViewSet)
luffyapi_router.register(r'courses_detail', courses_views.CoursesDetailModelViewSet)


urlpatterns = luffyapi_router.urls

urlpatterns.append(re_path('^online/$', account_views.AccountView.as_view({'post': 'login'})))
urlpatterns.append(re_path('^micro/$', micro_news_views.MicroView.as_view()))
