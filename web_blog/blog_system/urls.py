#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/25 18:55
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : urls.py
# @Software: PyCharm


from blog_system.views import Index
from django.urls import path


app_name = 'blog_system'
urlpatterns = [
    path(r'<str:pro_category_id>', Index.as_view(), name='index'),
]

