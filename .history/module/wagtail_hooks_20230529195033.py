from wagtail.admin.menu import admin_menu
from django.contrib.auth.models import Group
from wagtail.core import hooks

@hooks.register('construct_main_menu')
def hide_group_menu_item(request, menu_items):
    if not request.user.is_superuser:
        # 非管理员用户隐藏组菜单项
        menu_items[:] = [item for item in menu_items if item.name != 'groups']

@hooks.register('before_serve_page')
def restrict_group_editing(page, request, serve_args, serve_kwargs):
    if not request.user.is_superuser:
        # 非管理员用户重定向到首页，限制组的编辑和访问权限
        group_editing_path = '/admin/groups/'
        if request.path.startswith(group_editing_path):
            return redirect('/')

@hooks.register('construct_page_listing_buttons')
def remove_group_edit_buttons(buttons, page, page_perms, is_parent=False, context=None):
    if not context['request'].user.is_superuser:
        # 非管理员用户移除组的编辑按钮
        buttons[:] = [button for button in buttons if button.name != 'edit-group']

@hooks.register('register_group_action_menu_item')
def restrict_group_delete_actions(group):
    if not group.request.user.is_superuser:
        # 非管理员用户限制组的删除操作
        return []

@hooks.register('register_permissions')
def hide_group_permissions():
    return None

@hooks.register('register_group_permissions_panel')
def hide_group_permissions_panel():
    return None
