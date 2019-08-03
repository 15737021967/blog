#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/8/3 14:25
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : signals.py
# @Software: PyCharm
from django.db.models import signals
from django.dispatch import receiver
from user.models import EmailVerification
from user.notify import Notify


@receiver(signals.post_save, sender=EmailVerification)
def code_notify_post(instance, created, **kwargs):
    if created:
        Notify(instance.id).send_email()
