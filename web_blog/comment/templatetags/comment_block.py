#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/26 14:41
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : comment_block.py
# @Software: PyCharm
from django import template
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from comment.commentforms import CommentForm
from comment.models import Comment


register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(blog_id):

    user = get_object_or_404(User, post__id=blog_id)
    default = {
        'reply_to': user.userinfo.name,
        'reply_to_blog': blog_id,

    }

    return {
        'comment_form': CommentForm(initial=default),
        'comment_list': Comment.get_by_reply_to_blog(blog_id)
    }



