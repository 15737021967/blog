from .models import Comment, Snap
from web_blog.base_admin import BaseAuthorAdmin
import xadmin


@xadmin.sites.register(Comment)
class CommentAdmin(BaseAuthorAdmin):

    list_display = ('reply', 'reply_to_some', 'content', 'status', 'created_time')

    def reply_to_some(self, obj):

        return obj.reply_to_blog if obj.parent is None else obj.parent

    reply_to_some.short_description = '评论目标'


@xadmin.sites.register(Snap)
class SnapAdmin(object):

    list_display = ('post', 'user')

