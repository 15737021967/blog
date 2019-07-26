#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/7/23 18:42
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : commentforms.py
# @Software: PyCharm


from django import forms
from django.forms import fields
from django.forms import widgets
from user.models import UserInfo
from blog.models import Post
from .models import Comment


class CommentForm(forms.Form):

    content = fields.CharField(
        label='内容',
        max_length=2000,
        widget=widgets.TextInput()
    )

    parent = fields.CharField(
        widget=widgets.HiddenInput(),
        required=False,
    )

    reply_to = fields.CharField(
        widget=widgets.HiddenInput(),
    )

    reply_to_blog = fields.CharField(
        widget=widgets.HiddenInput(),
    )

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if len(parent) > 0:
            if not UserInfo.objects.filter(id=parent).exists():
                raise forms.ValidationError('操作异常')

        return parent

    def clean_reply_to(self):
        reply_to = self.cleaned_data.get('reply_to')
        if not UserInfo.objects.filter(name=reply_to).exists():
            raise forms.ValidationError('操作异常')

        return reply_to

    def clean_reply_to_blog(self):
        reply_to_blog = self.cleaned_data.get('reply_to_blog')
        if not Post.objects.filter(id=reply_to_blog).exists():
            raise forms.ValidationError('操作异常')

        return reply_to_blog
