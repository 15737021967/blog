#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/26 18:01
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : ValidationErrorTOJson.py
# @Software: PyCharm
from django.forms import ValidationError
import json


class JsonCustomEncoder(json.JSONEncoder):  # 处理函数，对特定数据类型进行处理
    def default(self, field):
        if isinstance(field, ValidationError):
            return {'code': field.code, 'message': field.message}  # 返回一个字典
        else:
            return json.JSONEncoder.default(self, field)
