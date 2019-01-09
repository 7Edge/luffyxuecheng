#! /usr/bin/env python3
# coding:utf-8
# author:zhangjiaqi<1399622866@qq.com>
# Date:2018-12-22

"""
课程相关视图
"""
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from ..models import Course, CourseDetail, Chapters
from ..serializers import CourseModelSerializer, CourseDetailModelSerializer, ChaptersModelSerializer


# from ..renders import CustomJsonRender


class CoursesModelViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    # content_negotiation_class = []


class CoursesDetailModelViewSet(ModelViewSet):
    queryset = CourseDetail.objects.all()
    serializer_class = CourseDetailModelSerializer


class ChapterModelViewSet(ModelViewSet):
    queryset = Chapters
    serializer_class = ChaptersModelSerializer


if __name__ == '__main__':
    pass
