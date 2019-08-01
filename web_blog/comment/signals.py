#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/8/1 15:21
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : signals.py
# @Software: PyCharm
from django.db.models import signals
from django.dispatch import receiver
from comment.models import Comment
from comment.Notify import Notify


@receiver(signals.post_save, sender=Comment)
def comment_notify_post(instance, created, **kwargs):
    if created:
        Notify(instance.id).send_email()






