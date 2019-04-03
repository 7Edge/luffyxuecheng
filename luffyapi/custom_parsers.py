#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: custom_parsers
# Date: 2/26/2019
# import json
#
# from rest_framework import renderers
#
# from luffyapi.utils.customer_response import BaseResponse
#
#
# # 继承JSON
# class JSONCustomParser(renderers.JSONRenderer):
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         ret = super().render(data, accepted_media_type, renderer_context)
#         ret_obj = json.loads(ret, encoding='utf-8')
#
#         response_obj = BaseResponse()
#         response_obj.data = ret_obj
#
#         return


if __name__ == '__main__':
    pass
