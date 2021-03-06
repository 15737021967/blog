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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from user.views import Register, Active, Login, EditUserInfo, Logout, ForgetPassword
from blog_system.views import Index
from rest_framework.routers import DefaultRouter
from blog.apis import PostViewSet, CategoryViewSet
import xadmin


router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')


urlpatterns = [
    re_path(r'^$', Index.as_view(), name="index"),
    path(r'api/', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path(r'xadmin/', xadmin.site.urls, name="xadmin"),
    path(r'register', Register.as_view(), name="register"),
    path(r'active/<str:code>', Active.as_view(), name="active"),
    path(r'login/', Login.as_view(), name="login"),
    path(r'logout/', Logout.as_view(), name="logout"),
    path(r'forget-password/', ForgetPassword.as_view(), name="forget-password"),
    path(r'edit_info/', EditUserInfo.as_view(), name="edit_info"),
    path(r'<str:auth>/', include('blog.urls')),
    path(r'nav/', include('blog_system.urls')),
    path(r'comment/', include('comment.urls')),
    path(r'mdeditor/', include('mdeditor.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
