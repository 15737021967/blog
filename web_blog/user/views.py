from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, reverse
from django.views.generic import View
from user.models import EmailVerification, UserInfo
from user.emailverification import range_code
from user.userforms import UserForm, LoginForms, EditInfo
from user.add_permissions import add_permissions
import json


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
            EmailVerification.objects.create(code=code, account=account, status=0)

        else:
            print(user_form.errors.as_data())
            return render(request, 'blog_system/user/register.html', context={'user': user_form})
        return HttpResponse(json.dumps('请进入邮箱激活账号'))

    def get(self, request):
        user_form = UserForm()
        return render(request, 'blog_system/user/register.html', context={'user': user_form})


class Login(View):
    """登陆模块"""
    def get(self, request):
        next_url = request.GET.get('next', '')
        print(next_url)
        return render(request, 'blog_system/user/login.html', context={'login_form': LoginForms(), 'next': next_url})

    def post(self, request):
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            login(request, authenticate(username=login_form.cleaned_data.get('account'),
                                        password=login_form.cleaned_data.get('password')))
            next_url = request.POST.get('next', '')
            print(next_url)
            if len(next_url) > 0:
                return redirect(next_url)
            return redirect(reverse("index"))
        else:
            print(login_form.errors.as_data())
            return render(request, 'blog_system/user/login.html', context={'login_form': login_form})


class Active(View):
    """账号激活模块"""
    http_method_names = ['get']

    def get(self, request, code):
        email_verification = get_object_or_404(EmailVerification, code=code)
        user = User.objects.filter(username=email_verification.account)
        user.update(is_active=True, is_staff=True)
        email_verification.delete()
        add_permissions(user[0])
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
        info = EditInfo(instance=user_info)
        return render(request, 'blog_system/user_info/personal_info.html',
                      context={'info_form': info, 'user_info': user_info})

    def post(self, request):
        rep = {
            'status': False,
            'msg': None,
            'info': None,
        }
        user_info = get_object_or_404(UserInfo, owner=request.user)
        info = EditInfo(request.POST, instance=user_info)
        if info.is_valid():
            info.save()
            rep['status'] = True
            rep['info'] = {
                'nickname': info.initial['nickname'],
                'sex': '未知' if info.initial['sex'] == 2 else '女' if info.initial['sex'] == 1 else '男',
                'birthday': info.initial['birthday'].strftime("%Y年%m月%d日"),
                'address': info.initial['address'],
                'introduction': info.initial['introduction'],
            }
        else:
            rep['msg'] = info.errors.as_json()
        return HttpResponse(json.dumps(rep))


class ForgetPassword(View):
    def get(self, request):
        return render(request, 'blog_system/forget_password.html', context={})

    def post(self, request):
        status = request.POST.get('status')
        if status == '1':
            account = request.POST.get('account')
            code = range_code(5)
            EmailVerification.objects.filter(status=1, account=account).delete()
            EmailVerification.objects.create(status=1, account=account, code=code)
            return HttpResponse(json.dumps('已经将验证码发至邮箱'))
        elif status == '2':
            account = request.POST.get('account')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            code = request.POST.get('code')
            email_info = EmailVerification.objects.filter(account=account, code=code)
            if not all([account, password, confirm_password, code]):
                return HttpResponse(json.dumps('请填写完整'))
            if confirm_password != password:
                return HttpResponse(json.dumps('请输入相同的密码'))
            if not email_info.exists():
                return HttpResponse(json.dumps('请出入正确的验证码'))
            else:
                email_info.delete()
                user = User.objects.get(username=account)
                user.set_password(password)
                user.save()
                return HttpResponse(json.dumps('密码重置成功'))
