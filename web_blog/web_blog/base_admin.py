class BaseOwnerAdmin(object):
    """
        1、用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
        2、用来针对queryset过滤当前用户的数据
    """

    exclude = ('owner', )

    def get_list_queryset(self):
        request = self.request
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        return qs.filter(owner=request.user)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super(BaseOwnerAdmin, self).save_models()


class BaseAuthorAdmin(object):

    def get_list_queryset(self):
        request = self.request
        qs = super(BaseAuthorAdmin, self).get_list_queryset()
        return qs.filter(reply_to_blog__owner=request.user)

