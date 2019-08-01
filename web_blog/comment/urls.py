#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/26 17:45
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : urls.py
# @Software: PyCharm

from django.urls import path
from comment.views import CommentView, SnapView

app_name="comment"
urlpatterns = [
    path(r'comment/', CommentView.as_view(), name="comment"),
    path(r'snap/', SnapView.as_view(), name="snap")
]
