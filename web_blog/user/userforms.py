from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import fields
from django.forms import widgets
from user.models import UserInfo


class UserForm(forms.Form):

    account = fields.EmailField(widget=widgets.EmailInput(attrs={'class': 'input-text', 'placeholder': '邮箱'}),
                                label="账号", required=False)
    password = fields.CharField(widget=widgets.PasswordInput(attrs={'class': 'input-text', 'placeholder': '密码'}),
                                label="密码", required=False)
    confirm_password = fields.CharField(widget=widgets.PasswordInput(
        attrs={'class': 'input-text', 'placeholder': '请再次输入密码'}), label="确定密码", required=False)
    name = fields.CharField(widget=widgets.Input(attrs={'class': 'input-text', 'placeholder': '用户名'}),
                            label="用户名", required=False)

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
        if password is None:
            return
        if password != confirm_password:
            raise forms.ValidationError(u"两次密码输入不一致，请重新输入")

        return password

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if UserInfo.objects.filter(name=name).exists():
            raise forms.ValidationError(u"该用户名已存在，请重新填写")

        return name


class LoginForms(forms.Form):

    account = fields.EmailField(widget=widgets.EmailInput(attrs={'class': 'input-text', 'placeholder': '邮箱'}),
                                label="账号", required=False)
    password = fields.CharField(widget=widgets.PasswordInput(attrs={'class': 'input-text', 'placeholder': '密码'}),
                                label="密码", required=False)

    def clean_password(self):

        account = self.cleaned_data.get('account')
        password = self.cleaned_data.get('password')
        if authenticate(username=account, password=password) is None:
            raise forms.ValidationError(u"请输入正确的账号和密码")

        return password


class EditInfo(forms.ModelForm):

    birthday = fields.DateTimeField(
        widget=widgets.DateInput(attrs={'type': 'date', 'class': 'el-input__inner'}),
        label='生日'
    )
    nickname = fields.CharField(widget=widgets.TextInput(
        attrs={'class': 'el-input__inner'}),
        label='昵称'
    )
    sex = fields.ChoiceField(
        widget=widgets.Select(attrs={'class': 'el-input__inner'}),
        label='性别',
        choices=((0, '男'), (1, '女'), (2, '未知'))
    )
    address = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'el-input__inner'}),
        label='地址'
    )
    introduction = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'textarea'}),
        label='简介'
    )

    class Meta:
        model = UserInfo
        fields = (
            'nickname', 'sex', 'birthday', 'address', 'introduction'
        )


