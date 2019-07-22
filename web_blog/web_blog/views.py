from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from apps.blogsystem.models import ProjectCategory


def index(request):
    pro_category = ProjectCategory.get_pro_category()
    return render(request, 'blogsystem/index.html', context={'pro_category': pro_category})


class Register(View):

    def post(self, request):
        cont = request.POST.get('id', None)
        pwd = request.POST.get('pwd', None)
        if cont and pwd:
            user = authenticate(username=cont, password=pwd)
            if user is None:
                User.objects.create_user(cont, cont, pwd)
                print('create successful!')
                return render(request, 'blogsystem/register.html', context={})

    def get(self, request):

        return render(request, 'blogsystem/register.html', context={})

