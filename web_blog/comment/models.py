from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
# Create your models here.


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    parent = models.ForeignKey('self', verbose_name="回复评论", null=True, on_delete=models.CASCADE, blank=True)
    reply = models.ForeignKey(User, verbose_name="回复者", on_delete=models.SET_NULL, null=True, related_name="replyer",
                              related_query_name="replyer")
    reply_to = models.ForeignKey(User, verbose_name="回复用户", on_delete=models.SET_NULL, null=True,
                                 related_name="replyto", related_query_name="replyto")
    reply_to_blog = models.ForeignKey(Post, verbose_name="回复博文", on_delete=models.CASCADE)
    content = models.CharField(max_length=2000, verbose_name="内容")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "评论"

    @classmethod
    def get_by_reply_to_blog(cls, blog_id):
        return cls.objects.filter(reply_to_blog_id=blog_id, status=cls.STATUS_NORMAL)

    @property
    def get_children_comment(self):
        content = Comment.objects.filter(reply_to=self)
        return content
