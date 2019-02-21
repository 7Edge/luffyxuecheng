#! /usr/bin/env python3
# coding:utf-8
# author:zhangjiaqi<1399622866@qq.com>
# Date:2018-12-22

"""
luffy学城api序列化类
"""
# import os
from rest_framework import serializers
from django.conf import settings

from .models import CourseDetail, Course, Chapters
from .models import UserInfo
from .models import CourseSubCategory, CourseCategory

from rest_framework.serializers import ListSerializer


# 专题课程序列化
class CourseModelSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='get_level_display')
    recommend_courses = serializers.SerializerMethodField()
    chapters = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'image', 'level', 'recommend_courses', 'chapters']

    def get_recommend_courses(self, obj):
        qs = obj.re_course.all()
        return [{'id': i.course.id, 're_course_title': i.course.title} for i in qs]

    def get_chapters(self, obj):
        if isinstance(self, ListSerializer):
            return ''
        qs = obj.chapters_set.all()
        return [{'id': j.id, 'chapter_name': j.title} for j in qs]

    def get_image(self, obj):
        rel_path = obj.image
        rely_on_path = settings.STATIC_URL
        return rely_on_path + rel_path


# 课程详情
class CourseDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = "__all__"
        depth = 1


# 章节详情
class ChaptersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapters
        fields = "__all__"


# 主课程分类
class CourseCategoryModelSerializer(serializers.ModelSerializer):
    subcategory_url = serializers.HyperlinkedRelatedField(source='coursesubcategory_set',
                                                          view_name='luffyapi:coursesubcategory-detail',
                                                          read_only=True,
                                                          many=True)

    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'subcategory_url']


# 子课程分类
class CourseSubCategoryModelSerializer(serializers.ModelSerializer):
    """
    子课程分类 序列化
    """
    category_url = serializers.HyperlinkedRelatedField(source='category', view_name='luffyapi:coursecategory-detail',
                                                       lookup_field='pk',
                                                       lookup_url_kwarg='pk', read_only=True)

    courses_url = serializers.HyperlinkedIdentityField(
        view_name='luffyapi:coursesubcategory-get-courses',
        read_only=True)

    class Meta:
        model = CourseSubCategory
        fields = ['id', 'name', 'category', 'category_url', 'courses_url']


# 用户密码序列化类
class UserPwdModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user', 'pwd']


if __name__ == '__main__':
    pass
