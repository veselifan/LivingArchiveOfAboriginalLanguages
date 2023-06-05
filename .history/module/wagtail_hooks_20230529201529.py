from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from wagtail.contrib.modeladmin.views import EditView

class CustomGroupEditView(EditView):
    model_admin = GroupAdmin
    template_name = 'admin/groups/4.html'

from wagtail.core import hooks
from .custom_views import CustomGroupEditView

@hooks.register('register_group_edit_view')
def register_custom_group_edit_view():
    return CustomGroupEditView.as_view()
