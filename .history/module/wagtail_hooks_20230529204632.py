from wagtail.admin.views.pages import PageListingView
from wagtail.core import hooks


@hooks.register('register_page_listing_buttons')
def hide_delete_button(buttons, page, page_perms, is_parent=False, context=None):
    group_name = 'test1'  # 替换为您要隐藏删除按钮的组名

    if page_perms.can_delete() and page_perms.user.groups.filter(name=group_name).exists():
        # 用户属于指定组，显示删除按钮
        return buttons
    else:
        # 用户不属于指定组，隐藏删除按钮
        return []
