from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, reverse
from django.views.generic import View
from blog_system.models import ProjectCategory
from user.models import EmailVerification, UserInfo
from web_blog.emailverification import range_code, email_message
from user.userforms import UserForm, LoginForms, EditInfo
from blog.models import Post
import json
# import json


def index(request):
    """网站的主页"""
    pro_category_list = ProjectCategory.get_pro_category()
    post_list = Post.objects.filter(pro_category=1)
    pro_category = get_object_or_404(ProjectCategory, id=1)
    return render(request, 'blog_system/index.html',
                  context={
                      'pro_category_list': pro_category_list, 'post_list': post_list, 'pro_category': pro_category
                    }
                  )


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
        next_url = request.GET.get('next', '')
        print(next_url)
        return render(request, 'blog_system/login.html', context={'login_form': LoginForms(), 'next': next_url})

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
            return render(request, 'blog_system/login.html', context={'login_form': login_form})


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
