#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/23 11:43
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : urls.py
# @Software: PyCharm


from django.urls import path
from blog import views

app_name = 'post'
urlpatterns = [
    path(r'index/', views.IndexView.as_view(), name='post-list'),
    path(r'article/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail'),
    path(r'category/<int:category_id>/', views.CategoryView.as_view(), name='category-list'),

]
