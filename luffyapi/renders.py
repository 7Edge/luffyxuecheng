#! /usr/bin/env python3
# coding:utf-8
# author:zhangjiaqi<1399622866@qq.com>
# Date:2018-12-29

"""
渲染器
"""
from rest_framework import renderers


class CustomJsonRender(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        new_data = {
            'code': 10000,
            'data': data,
        }
        return super().render(new_data, accepted_media_type, renderer_context)


if __name__ == '__main__':
    pass
