#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/23 11:43
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : urls.py
# @Software: PyCharm


from django.urls import path, re_path
from apps.blog import views


urlpatterns = [
    path(r'<str:auth>/', views.IndexView.as_view()),
    path(r'<str:auth>/<int:post_id>', views.DetailView.as_view()),
]
