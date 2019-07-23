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
from .models import Comment


class CommentForm(forms.ModelForm):

    content = fields.CharField(
        label='内容',
        max_length=2000,
        widget=widgets.TextInput()
    )

    class Meta:
        model = Comment
        fields = ['content', ]
