from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

from user_group_management.views import group_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return group_viewset


@hooks.register('construct_main_menu')
def add_user_group_management_menu_item(request, menu_items):
    if not request.user.groups.filter(name='contributor').exists():
        menu_items.append(MenuItem('User Group', '/admin/my-groups/', classnames='icon icon-group', order=10000))
        menu_items[:] = menu_items[-1:]


