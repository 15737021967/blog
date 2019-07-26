from .models import Comment
import xadmin


@xadmin.sites.register(Comment)
class CommentAdmin(object):

    list_display = ('reply', 'reply_to_some', 'content', 'status', 'created_time')

    def reply_to_some(self, obj):

        return obj.reply_to if obj.reply_to_blog is None else obj.reply_to_blog

    reply_to_some.short_description = '评论目标'
