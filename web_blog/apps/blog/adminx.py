from xadmin.layout import Row, Fieldset
from web_blog.base_admin import BaseOwnerAdmin
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
import xadmin


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):

    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'owner', )
    list_fields = ('name', 'status', 'is_nav', )

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):

    list_display = ('name', 'status', 'created_time', 'owner')
    list_fields = ('name', 'status')


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = (
        'title', 'category', 'status',
        'created_time', 'owner',
    )
    list_display_link = ()

    list_filter = ['category']
    search_fields = ('title', 'category__name')
    date_hierarchy = 'created_time'

    actions_on_top = True
    actions_on_bottom = False

    save_on_top = True

    exclude = ('owner', 'pv', 'uv')
    form_layout = (
        Fieldset(
            '基础配置',
            Row('title', 'category'),
            Row('pro_category', 'status', ),
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'contend_ck',
            'contend_md',
            'content',
        )
    )
