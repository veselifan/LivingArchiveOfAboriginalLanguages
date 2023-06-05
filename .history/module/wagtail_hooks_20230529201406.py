from django.urls import reverse
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView, WMABaseView

from django.contrib.auth.models import Group
from wagtail.users.views.groups import GroupEditView


class CustomGroupEditView(EditView):
    model_admin = GroupAdmin
    template_name = 'admin/groups/group_edit.html'


@hooks.register('register_group_edit_view')
def register_custom_group_edit_view():
    return CustomGroupEditView.as_view()

class CustomGroupEditView(WMABaseView):
    def __init__(self, model_admin):
        super().__init__(model_admin)
        self.delete_url = reverse('wagtailusers_groups_delete', args=[self.request.group.pk])

    def get_delete_url(self):
        return self.delete_url

    def delete(self, request, *args, **kwargs):
        return self.redirect('wagtailusers_groups_index')

def assign_permissions_to_group():
    group = Group.objects.get(name='test1')
    group.permissions.clear()
    # 添加其他权限到组中

class CustomGroupModelAdmin(ModelAdmin):
    model = Group
    index_view_class = IndexView
    edit_view_class = CustomGroupEditView

# 注册自定义 ModelAdmin
modeladmin_register(CustomGroupModelAdmin)

# 分配权限到组
assign_permissions_to_group()
