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
from django.views.decorators.cache import cache_page
from rest_framework import routers

from luffyapi.views import courses_views
from luffyapi.views import account_views
from luffyapi.views import micro_news_views

luffyapi_router = routers.SimpleRouter()
luffyapi_router.register(r'courses', courses_views.CoursesModelViewSet)
luffyapi_router.register(r'courses_detail', courses_views.CoursesDetailModelViewSet)
luffyapi_router.register(r'course_category', courses_views.CourseCategoryModelViewSet)
luffyapi_router.register(r'course_sub_category', courses_views.CourseSubCategoryModelViewSet)

auto_urlpatterns = luffyapi_router.urls
urlpatterns = auto_urlpatterns + [
    re_path('^online/$', account_views.AccountView.as_view({'post': 'login', 'get': 'get'})),
    re_path('^micro/$', cache_page(60*5)(micro_news_views.MicroView.as_view())),
    # re_path('course_sub_category/(?P<pk>)/courses/$',
    #         courses_views.CourseSubCategoryModelViewSet.as_view(actions={'get': 'get_courses'}))
]
