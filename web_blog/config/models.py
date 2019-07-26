from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
# Create your models here.


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")  # 默认长度为200
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    weight = models.PositiveIntegerField(default=1, choices=zip(
                                        range(1, 6), range(1, 6)), verbose_name="权重", help_text="权重高展示顺序靠前")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "友链"


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    DISPLAY_CATEGORY = 5
    DISPLAY_INTERFILE = 6
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
        (DISPLAY_CATEGORY, '个人分类'),
        (DISPLAY_INTERFILE, '归档'),
    )
    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, verbose_name="内容", help_text="如果设置的不是 HTML 类型，可为空")
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.SET_NULL, null=True)
    weight = models.IntegerField(default=-1, verbose_name="权重")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        ordering = ['weight', '-created_time']
        verbose_name = verbose_name_plural = "侧边栏"

    @classmethod
    def get_all(cls, auth_obj):
        return cls.objects.filter(status=cls.STATUS_SHOW, owner=auth_obj)

    @property
    def content_html(self):
        """ 直接渲染模板 """
        from blog.models import Post, Category
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            posts = Post.latest_posts(self.owner, with_related=False)
            if len(posts) > 5:
                posts = posts[:5]
            content = {
                'posts': posts
            }
            result = render_to_string('config/sidebar_posts.html', content)
        elif self.display_type == self.DISPLAY_HOT:
            posts = Post.hot_posts(self.owner)
            if len(posts) > 5:
                posts = posts[:5]
            content = {
                'posts': posts
            }
            result = render_to_string('config/sidebar_posts.html', content)
        elif self.display_type == self.DISPLAY_COMMENT:
            comments = Comment.objects.filter(
                reply_to_blog__in=Post.objects.filter(owner=self.owner)
            ).order_by('-created_time')
            if len(comments) > 5:
                comments = comments[:5]
            content = {
                'comments': comments
            }
            result = render_to_string('config/sidebar_comments.html', content)
        elif self.display_type == self.DISPLAY_CATEGORY:
            content = {
                'categories': Category.get_categories(self.owner)
            }
            result = render_to_string('config/sidebar_category.html', content)
        # elif self.display_type == self.DISPLAY_INTERFILE:
        #     content = {
        #
        #     }
        #     result = render_to_string('', content)
        return result
