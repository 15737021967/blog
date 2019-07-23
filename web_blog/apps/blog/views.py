from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, F
from .models import Post, Category, Tag
from apps.config.models import SideBar
from apps.user.models import UserInfo
from apps.comment.commentforms import CommentForm
from apps.comment.models import Comment
# Create your views here.


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.kwargs.get('auth')
        auth_obj = get_object_or_404(User, userinfo__name=auth)
        context.update({
            'sidebars': SideBar.get_all(auth_obj),
        })
        context.update(Category.get_navs(auth_obj))
        return context


class IndexView(CommonViewMixin, ListView):
    def get_queryset(self):
        auth = self.kwargs.get('auth')
        auth_obj = get_object_or_404(User, userinfo__name=auth)
        queryset = Post.latest_posts(auth_obj)
        return queryset

    paginate_by = 10
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class PostDetailView(CommonViewMixin, DetailView):
    """博客详情页面"""
    def get_queryset(self):
        auth = self.kwargs.get('auth')
        print(auth)
        auth_obj = get_object_or_404(User, userinfo__name=auth)
        queryset = Post.latest_posts(auth_obj)
        return queryset

    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        print(post_id)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_reply_to_blog(post_id)
        })
        return context
