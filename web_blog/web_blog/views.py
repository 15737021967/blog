from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, reverse
from django.views.generic import View
from apps.blog_system.models import ProjectCategory
from apps.user.models import EmailVerification, UserInfo
from .emailverification import range_code, email_message
from .userforms import UserForm, LoginForms, EditInfo

# import json


def index(request):
    """网站的主页"""
    pro_category = ProjectCategory.get_pro_category()
    return render(request, 'blog_system/index.html', context={'pro_category': pro_category})


class Register(View):
    """注册模块"""
    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            account = user_form.cleaned_data.get('account')
            pwd = user_form.cleaned_data.get('password')
            name = user_form.cleaned_data.get('name')
            user = User.objects.create_user(account, account, pwd, is_active=False)
            UserInfo.objects.create(owner=user, name=name, nickname=name)
            code = range_code()
            EmailVerification.objects.create(account=account, status=EmailVerification.STATUS_REGISTER, code=code)
            message = email_message(code)
            send_mail('账号激活', message, '1531391246@qq.com', ['1531391246@qq.com', ])
            print('create successful!')

        else:
            print(user_form.errors.as_data())
            return render(request, 'blog_system/register.html', context={'user': user_form})
        return render(request, 'blog_system/register.html', context={'user': UserForm()})

    def get(self, request):
        user_form = UserForm()
        return render(request, 'blog_system/register.html', context={'user': user_form})


class Login(View):
    """登陆模块"""
    def get(self, request):

        return render(request, 'blog_system/login.html', context={'login_form': LoginForms()})

    def post(self, request):
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            login(request, authenticate(username=login_form.cleaned_data.get('account'),
                                        password=login_form.cleaned_data.get('password')))
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            print(next_url)
            return redirect(reverse("index"))
        else:
            return render(request, 'blog_system/login.html', context={'login_form': LoginForms()})


class Active(View):
    """账号激活模块"""
    http_method_names = ['get']

    def get(self, request, code):
        email_verification = get_object_or_404(EmailVerification, code=code)
        User.objects.filter(username=email_verification.account).update(is_active=True, is_staff=True)
        email_verification.delete()
        return HttpResponse("你已激活账号")


class Logout(View):
    """注销模块"""
    http_method_names = ['get']

    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class EditUserInfo(LoginRequiredMixin, View):
    """用户信息填写"""
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user_info = get_object_or_404(UserInfo, owner=request.user)
        info = EditInfo(user_info)
        return render(request, 'blog_system/edit_info.html', context={'user_info': info})

    def post(self, request):
        info = EditInfo(request.POST)
        if info.is_valid():
            user_info = get_object_or_404(UserInfo, owner=request.user)
            user_info.update(*info)

        return render(request, 'blog_system/edit_info.html', context={'user_info': info})
