from wagtail.core import hooks
from django.contrib.auth.models import Group

@hooks.register('construct_page_listing_buttons')
def remove_delete_button_for_group(buttons, page, page_perms, is_parent=False, context=None):
    # 获取当前用户所属的组
    user_groups = Group.objects.filter(user=context['request'].user)

    # 检查当前用户是否属于特定组（这里是 'test1'）
    if user_groups.filter(name='test1').exists():
        # 如果用户属于 test1 组，则移除删除按钮
        buttons[:] = [button for button in buttons if button.name != 'delete']

    # 返回更新后的按钮列表
    return buttons
