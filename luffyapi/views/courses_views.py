#! /usr/bin/env python3
# coding:utf-8
# author:zhangjiaqi<1399622866@qq.com>
# Date:2018-12-22

"""
课程相关视图
"""
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from ..models import Course, CourseDetail, Chapters, CourseSubCategory, CourseCategory
from ..serializers import CourseModelSerializer, CourseDetailModelSerializer, ChaptersModelSerializer
from ..serializers import CourseSubCategoryModelSerializer, CourseCategoryModelSerializer


# 课程主分类ViewSet
class CourseCategoryModelViewSet(ModelViewSet):
    queryset = CourseCategory.objects.all().order_by('pk')
    serializer_class = CourseCategoryModelSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    # from rest_framework.versioning import URLPathVersioning
    # versioning_class = URLPathVersioning


# 课程子类
class CourseSubCategoryModelViewSet(ReadOnlyModelViewSet):
    """
    课程子类，支持读取，由于分类少不分页，支持获取获取子类下的课程（子类课程支持分页）
    """
    queryset = CourseSubCategory.objects.all()
    serializer_class = CourseSubCategoryModelSerializer
    lookup_url_kwarg = 'pk'
    pagination_class = None

    # 获取课程之类下的所有课程
    @action(methods=['get'], detail=True, url_path='courses')
    def get_courses(self, request, *args, **kwargs):
        num_paginator = PageNumberPagination()
        num_paginator.page_size_query_param = 'page_size'
        subcategory_obj = self.get_object()
        courses = subcategory_obj.course_set.all().order_by('id')
        page_courses = num_paginator.paginate_queryset(courses, request, view=self)
        serializer_obj = CourseModelSerializer(page_courses, many=True)
        return num_paginator.get_paginated_response(serializer_obj.data)


# 专题课
class CoursesModelViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by('pk')
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
