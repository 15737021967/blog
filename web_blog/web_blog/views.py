from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from apps.blogsystem.models import ProjectCategory
from .userforms import UserForm
import json


def index(request):
    pro_category = ProjectCategory.get_pro_category()
    return render(request, 'blogsystem/index.html', context={'pro_category': pro_category})


class Register(View):

    def post(self, request):
        userform = UserForm(request.POST)
        if userform.is_valid():
            account = userform.cleaned_data.get('account')
            pwd = userform.cleaned_data.get('password')
            User.objects.create_user(account, account, pwd, is_active=False)
            print('create successful!')

        else:
            print(userform.errors.as_data())
            return render(request, 'blogsystem/register.html', context={'user': userform})
        return render(request, 'blogsystem/register.html', context={'user': UserForm()})

    def get(self, request):
        userform = UserForm()
        return render(request, 'blogsystem/register.html', context={'user': userform})


class Login(View):

    def get(self):
        pass

    def post(self):
        pass
