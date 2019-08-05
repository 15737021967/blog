from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from blog.models import Post
from blog_system.models import ProjectCategory


# Create your views here.


class IndexViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pro_category_id = self.kwargs.get('pro_category_id') or -1
        if pro_category_id == -1:
            pro_category = get_object_or_404(ProjectCategory, name="推荐")
        else:
            pro_category = get_object_or_404(ProjectCategory, id=pro_category_id)
        context.update({
            'pro_category_list': ProjectCategory.get_pro_category(),
            'pro_category': pro_category
        })
        return context


class Index(IndexViewMixin, ListView):

    def get_queryset(self):
        pro_category_id = self.kwargs.get('pro_category_id') or -1
        if pro_category_id == -1:
            queryset = Post.objects.all().order_by('-created_time')[:100]
        else:
            queryset = Post.objects.filter(pro_category_id=pro_category_id)[:100]
        return queryset

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs):
        return super(Index, self).get(request, *args, **kwargs)

    paginate_by = 10
    template_name = 'blog_system/index.html'
    context_object_name = 'post_list'



