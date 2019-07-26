from datetime import date
from django.core.cache import cache
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import F
from .models import Post, Category, Tag
from config.models import SideBar
from comment.commentforms import CommentForm
from comment.models import Comment

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


class CategoryView(IndexView):
    """根据分类查看文章"""
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        auth = self.kwargs.get('auth')
        auth_obj = get_object_or_404(User, userinfo__name=auth)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, owner=auth_obj)

    def get_queryset(self):
        queryset = super(CategoryView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    """根据标签查看文章"""
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super(TagView, self).get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    """博客详情页面"""
    def get_queryset(self):
        auth = self.kwargs.get('auth')
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
            cache.set(uv_key, 1, 60*60*2)
        if increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)

