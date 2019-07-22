from .models import ProjectCategory
import xadmin


@xadmin.sites.register(ProjectCategory)
class ProjectCategoryAdmin(object):

    list_display = ('name', 'status', 'created_time')
    list_field = ('name', 'status', 'created_time',)

