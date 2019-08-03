#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/8/3 14:21
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : notify.py
# @Software: PyCharm
from django.core.mail import send_mail
from user.models import EmailVerification
from user.emailverification import email_message


class Notify(object):

    def __init__(self, e_id):
        self.e_id = e_id
        self.sender = '1531391246@qq.com'

    def send_email(self):
        email_info = EmailVerification.objects.get(id=self.e_id)

        smap = {
            0: [{
                'subject': ['账号激活'],
                'message': email_message(email_info.code),
                'receiver_list': [email_info.account],
            }],
            1: [{
                'subject': ['找回密码'],
                'message': '您的验证码为' + email_info.code,
                'receiver_list': [email_info.account],
            }],
        }
        _list = smap[email_info.status]
        for item in _list:
            try:
                send_mail(
                    item['subject'],
                    item['message'],
                    self.sender,
                    item['receiver_list'],
                )
            except Exception as e:
                print(e)
