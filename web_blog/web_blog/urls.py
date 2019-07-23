"""web_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from .views import index, Register, Active, Login, EditUserInfo
import xadmin

urlpatterns = [
    re_path(r'^$', index, name="index"),
    path(r'admin/', admin.site.urls),
    path(r'xadmin/', xadmin.site.urls, name="xadmin"),
    path(r'ckeditor/', include('ckeditor_uploader.urls')),
    path(r'register', Register.as_view(), name="register"),
    path(r'active/<str:code>', Active.as_view(), name="active"),
    path(r'login/', Login.as_view(), name="login"),
    path(r'editinfo/', EditUserInfo.as_view(), name="edit_info"),
    path(r'blog/', include('apps.blog.urls')),
]
