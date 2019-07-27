from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from blog.models import Post
from blog_system.models import ProjectCategory


# Create your views here.


class IndexViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pro_category_id = self.kwargs.get('pro_category_id')
        pro_category = get_object_or_404(ProjectCategory, id=pro_category_id)
        context.update({
            'pro_category_list': ProjectCategory.get_pro_category(),
            'pro_category': pro_category
        })
        return context


class Index(IndexViewMixin, ListView):

    def get_queryset(self):
        pro_category_id = self.kwargs.get('pro_category_id')
        queryset = Post.objects.filter(pro_category_id=pro_category_id)
        return queryset

    paginate_by = 10
    template_name = 'blog_system/index.html'
    context_object_name = 'post_list'



