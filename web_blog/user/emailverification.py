#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/23 9:32
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : emailverification.py
# @Software: PyCharm


import random


def range_code(max_length=50):
    """返回激活账号的链接"""
    str_pool = 'abcdefghijklmnopqrstuvwxyz123456798ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = [random.choice(str_pool) for i in range(max_length)]
    str_code = ''.join(code)
    return str_code


def email_message(code):
    """构建邮件信息"""
    str_message = '请点击以下链接来激活账号：http://127.0.0.1:8010/active/' + code
    return str_message
