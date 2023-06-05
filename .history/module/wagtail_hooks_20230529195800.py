from wagtail.core import hooks
from wagtail.users.views import groups as wagtail_groups_views

@hooks.register('before_serve_wagtailadmin_group_edit')
def restrict_group_edit(request, group_id):
    if not request.user.is_superuser:
        # 如果当前用户不是超级用户，则重定向到列表页面或其他适当的操作
        return redirect('admin_groups_list')  # 替换为你想要重定向的 URL

@hooks.register('before_serve_wagtailadmin_group_delete')
def restrict_group_delete(request, group_id):
    if not request.user.is_superuser:
        # 如果当前用户不是超级用户，则重定向到列表页面或其他适当的操作
        return redirect('admin_groups_list')  # 替换为你想要重定向的 URL

# 注册自定义的视图
wagtail_groups_views.group_edit = restrict_group_edit
wagtail_groups_views.group_delete = restrict_group_delete
