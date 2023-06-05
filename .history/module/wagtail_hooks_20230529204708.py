from wagtail.admin.menu import MenuItem
from wagtail.admin.menu import menu_item
from wagtail.core import hooks
from wagtail.users.models import Group

@hooks.register('register_group_permission_panel')
def hide_group_menu_item():
    class HideGroupMenuItem(MenuItem):
        def is_shown(self, request):
            # 获取当前用户
            user = request.user

            # 检查用户是否属于指定的组
            group_name = "test1"  # 替换为要隐藏删除按钮的组名
            try:
                group = Group.objects.get(name=group_name)
                if group in user.groups.all():
                    return False
            except Group.DoesNotExist:
                pass

            return True

    return HideGroupMenuItem(
        _('Groups'), reverse('wagtailgroups:index'),
        name='groups', classnames='icon icon-group',
        attrs={'data-test': 'groups'}
    )
