#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/8/28 10:32
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : apis.py
# @Software: PyCharm
from rest_framework import viewsets
from .serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer
from .models import Post, Category


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """提供文章接口"""
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """提供分类接口"""
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)

