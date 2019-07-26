from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserInfo(models.Model):
    owner = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name="账号")
    name = models.CharField(max_length=50, verbose_name="用户名", unique=True)
    nickname = models.CharField(max_length=50, verbose_name="昵称", null=True)
    sex = models.PositiveSmallIntegerField(default=2, choices=((0, '男'), (1, '女'), (2, '未知')), verbose_name="性别",
                                           null=True, blank=True)
    birthday = models.DateField(null=True, verbose_name="生日", blank=True)
    introduction = models.CharField(max_length=254, verbose_name="个人描述", default="该用户很懒，什么也没有留下...", blank=True)
    address = models.CharField(max_length=50, null=True, default="未知", blank=True, verbose_name="地址")

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "个人信息"


class EmailVerification(models.Model):
    STATUS_REGISTER = 0
    STATUS_FORGET = 1
    STATUS_ITEM = (
        (STATUS_FORGET, '忘记密码'),
        (STATUS_REGISTER, '邮箱注册')
    )
    account = models.EmailField(verbose_name="账号")
    status = models.PositiveIntegerField(choices=STATUS_ITEM, verbose_name="状态")
    code = models.CharField(max_length=64, verbose_name="验证码")

    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "邮箱验证"
