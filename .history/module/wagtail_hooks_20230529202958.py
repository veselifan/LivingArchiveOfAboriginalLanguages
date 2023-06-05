from wagtail.core import hooks
from wagtail.admin.action_menu import ActionMenuItem


@hooks.register('construct_page_action_menu')
def restrict_delete_button(menu_items, request, context):
    # 从菜单项列表中找到删除按钮并移除
    for i, menu_item in enumerate(menu_items):
        if menu_item.name == 'delete':
            menu_items.pop(i)
            break


# 注册一个新的菜单项，用于在设置页面中的组 "test1" 中显示删除按钮
@hooks.register('construct_page_action_menu')
def add_delete_button_for_test1(menu_items, request, context):
    group_name = 'test1'  # 替换为您要显示删除按钮的组名

    # 检查当前用户是否属于 "test1" 组
    if request.user.groups.filter(name=group_name).exists():
        # 创建一个新的删除按钮菜单项，并添加到菜单项列表
        delete_menu_item = ActionMenuItem('delete', 'Delete', 'delete', classnames='action-secondary')
        menu_items.append(delete_menu_item)
