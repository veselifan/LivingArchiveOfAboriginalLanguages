from wagtail.admin.widgets import Button
from wagtail.core import hooks


@hooks.register('construct_page_listing_buttons')
def remove_delete_button_for_test1_group(buttons, page, page_perms, context=None):
    user_groups = page_perms.user.groups.values_list('name', flat=True)

    if 'test1' in user_groups:
        # 遍历页面列表按钮
        for button in buttons:
            if isinstance(button, Button) and button.name == 'delete':
                # 移除删除按钮
                buttons.remove(button)
                break
