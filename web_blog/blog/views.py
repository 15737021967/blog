from datetime import date
from django.core.cache import cache
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from django.db.models import F
from .models import Post, Category
from config.models import SideBar
from comment.models import Snap

# Create your views here.


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.kwargs.get('auth')
        auth_obj = get_object_or_404(User, userinfo__name=auth)
        context.update({
            'sidebars': SideBar.get_all(auth_obj),
            'auth': auth
        })
        return context


class IndexView(CommonViewMixin, ListView):
    def get_queryset(self):
        auth = self.kwargs.get('auth')
        auth_obj = get_object_or_404(User, userinfo__name=auth)
        queryset = Post.latest_posts(auth_obj)
        return queryset

    @method_decorator(cache_page(60 * 1))
    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)

    paginate_by = 10
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    """根据分类查看文章"""
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context.update({
            'category': category,
        })
        return context

    @method_decorator(cache_page(60 * 1))
    def get(self, request, *args, **kwargs):
        return super(CategoryView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(CategoryView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class PostDetailView(CommonViewMixin, DetailView):
    """博客详情页面"""
    def get_queryset(self):
        auth = self.kwargs.get('auth')
        auth_obj = get_object_or_404(User, userinfo__name=auth)
        queryset = Post.latest_posts(auth_obj)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        if not self.request.user.is_authenticated:
            snap = False
        else:
            snap = Snap.objects.filter(post_id=post_id, user=self.request.user)
        context.update({
            'snap': snap
        })
        return context

    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    @method_decorator(cache_page(60 * 1))
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_uv = False
        uid = self.request.uid
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 60*60*24)
        if increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)
