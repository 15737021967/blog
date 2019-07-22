from django import forms
from django.forms import fields
from django.forms import widgets
from django.contrib.auth.models import User


class UserForm(forms.Form):

    account = fields.EmailField(widget=widgets.EmailInput(), label="账号", required=False)
    password = fields.CharField(widget=widgets.PasswordInput(), label="密码", required=False)
    confirm_password = fields.CharField(widget=widgets.PasswordInput(), label="确定密码", required=False)

    def clean_account(self):
        account = self.cleaned_data.get('account')
        user = User.objects.filter(username=account).exists()
        if user:
            raise forms.ValidationError(u"该邮箱已经注册过了")

        return account

    def clean_password(self):

        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError(u"你的密码长度太短了")
        elif len(password) > 20:
            raise forms.ValidationError(u"你的密码长度太长了")

        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(u"两次密码输入不一致，请重新输入")

        return password
