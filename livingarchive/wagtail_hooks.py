from django.urls import reverse
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks


@hooks.register('register_admin_menu_item')
def register_group_menu_item():
    return MenuItem('My Usergroup', reverse('group_list'), classnames='icon icon-group',
                    order=10000)


@hooks.register('construct_main_menu')
def add_user_group_management_menu_item(request, menu_items):
    print([i.name for i in menu_items])
    user = request.user
    if not user.is_superuser:
        if not user.groups.filter(name='Admin').exists():
            menu_items[:] = [item for item in menu_items if item.name != 'settings']
