#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2019/8/1 15:28
# @Author : Tan 
# @Email : 1531391246@qq.com
# @File : Notify.py
# @Software: PyCharm
from django.core.mail import send_mail
from comment.models import Comment


class Notify(object):
    def __init__(self, c_id):
        self.c_id = c_id
        self.ip = 'http://127.0.0.1:8000'

    def send_email(self):
        obj = Comment.objects.get(id=self.c_id)
        user = obj.reply.userinfo.name
        context = obj.content
        email_address = obj.reply_to.username
        auth = obj.reply_to_blog.owner.userinfo.name
        title = obj.reply_to_blog.title
        blog_id = obj.reply_to_blog.id
        msg = '#Re:%s\r\n%s:%s\r\n\r\n----------------\r\n作者:%s/%s\r\n地址:%s/%s/%s' % \
              (title, user, context, self.ip, auth, self.ip, auth, blog_id)
        send_mail('[PDBG博客评论通知]', msg, '1531391246@qq.com', [email_address])



