from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from mdeditor.fields import MDTextField
from blog_system.models import ProjectCategory
import mistune
# from django.utils.functional import cached_property
# Create your models here.


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "个人分类"

    def __str__(self):
        return self.name

    @classmethod
    def get_categories(cls, auth_obj):
        return cls.objects.filter(status=cls.STATUS_NORMAL, owner=auth_obj).annotate(post_count=Count('post'))


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    pv = models.PositiveIntegerField(default=1, verbose_name="点赞量")
    uv = models.PositiveIntegerField(default=1, verbose_name="浏览量")
    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = MDTextField(verbose_name="正文")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="个人分类", on_delete=models.SET_NULL, null=True)
    pro_category = models.ForeignKey(ProjectCategory, verbose_name="系统分类", on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.SET_NULL, null=True)
    content_html = models.TextField(verbose_name="正文html代码", blank=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']  # 根据id进行降序排序

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_repilated('owner', 'category')

        return post_list, category

    @classmethod
    def latest_posts(cls, auth_obj, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL, owner=auth_obj)
        if with_related:
            queryset = queryset.select_related('category')
        return queryset

    @classmethod
    def hot_posts(cls, auth_obj):
        return cls.objects.filter(status=cls.STATUS_NORMAL, owner=auth_obj).order_by('-uv')

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super(Post, self).save(*args, **kwargs)

    # @cached_property
    # def tags(self):
    #     return ','.join(self.tag.values_list('name', flat=True))
