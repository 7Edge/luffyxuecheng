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
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Course, CourseDetail, Chapters, CourseSubCategory, CourseCategory
from ..serializers import CourseModelSerializer, CourseDetailModelSerializer, ChaptersModelSerializer
from ..serializers import CourseSubCategoryModelSerializer, CourseCategoryModelSerializer


# from ..renders import CustomJsonRender


# 课程主分类ViewSet
class CourseCategoryModelViewSet(ModelViewSet):
    queryset = CourseCategory.objects.all().order_by('-pk')
    serializer_class = CourseCategoryModelSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    # from rest_framework.versioning import URLPathVersioning
    # versioning_class = URLPathVersioning


class CourseSubCategoryModelViewSet(ModelViewSet):
    queryset = CourseSubCategory.objects.all()
    serializer_class = CourseSubCategoryModelSerializer
    lookup_url_kwarg = 'pk'

    # 获取课程之类下的所有课程
    @action(methods=['get'], detail=True, url_path='courses')
    def get_courses(self, request, *args, **kwargs):
        subcategory_obj = self.get_object()
        courses = subcategory_obj.course_set.all()
        serializer_obj = CourseModelSerializer(courses, many=True)
        return Response(serializer_obj.data)


# 专题课
class CoursesModelViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    # content_negotiation_class = []


class CoursesDetailModelViewSet(ModelViewSet):
    queryset = CourseDetail.objects.all()
    serializer_class = CourseDetailModelSerializer


class ChapterModelViewSet(ModelViewSet):
    queryset = Chapters.objects.all()
    serializer_class = ChaptersModelSerializer


if __name__ == '__main__':
    pass
