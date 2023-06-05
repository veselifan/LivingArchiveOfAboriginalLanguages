from wagtail.admin.menu import MenuItem
from wagtail.core import hooks


@hooks.register('register_settings_menu_item')
def hide_group_menu_item(request):
    group_name = 'test1'  # 替换为您要隐藏的组名

    if request.user.groups.filter(name=group_name).exists():
        # 用户属于指定组，显示组菜单项
        return MenuItem('Group', '/admin/group/', classnames='icon icon-group', order=200)
    else:
        # 用户不属于指定组，隐藏组菜单项
        return None
