from web_blog.base_admin import BaseOwnerAdmin
from .models import SideBar, Link
import xadmin


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):

    list_display = ('title', 'display_type', 'content', 'created_time')
    list_field = ('title', 'display', 'content',)
