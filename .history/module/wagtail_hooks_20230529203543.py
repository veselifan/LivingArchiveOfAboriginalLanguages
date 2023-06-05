from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse


@hooks.register('register_admin_menu_item')
def register_group_dashboard_menu_item():
    return MenuItem('Group Dashboard', reverse('group_dashboard'), classnames='icon icon-group', order=200)
