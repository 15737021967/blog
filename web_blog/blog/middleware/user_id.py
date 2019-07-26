#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/24 16:37
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : user_id.py
# @Software: PyCharm


import uuid


USER_KEY = 'uid'
ONE_DAY = 60 * 60 * 24


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=ONE_DAY, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid

