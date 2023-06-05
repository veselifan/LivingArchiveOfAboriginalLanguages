from wagtail.core import hooks
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden

@hooks.register('construct_group_listing_buttons')
def disable_delete_group_button(buttons, group, request):
    # 检查当前用户是否属于 "普通用户组"
    if request.user.groups.filter(name='普通用户组').exists():
        # 禁止删除按钮
        buttons.pop('delete')
