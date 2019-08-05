#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/8/4 18:12
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : add_permissions.py
# @Software: PyCharm
from django.contrib.auth.models import Group


def add_permissions(user):
    group = Group.objects.get(name='blog_user')
    user.groups.add(group)




