from wagtail.core import hooks
from wagtail.admin.views.pages.edit import page_edit


@hooks.register('register_group_permission_panel')
def remove_group_delete_button():
    group_name = 'test1'  # 替换为您要移除删除按钮的组名

    # 获取删除按钮的索引位置
    delete_button_index = None
    for i, panel in enumerate(page_edit.edit_handler.children):
        if panel.__class__.__name__ == 'DeletePanel':
            delete_button_index = i
            break

    if delete_button_index is not None:
        # 移除删除按钮
        page_edit.edit_handler.children.pop(delete_button_index)

        # 获取所有注册的页面视图
        page_views = [view for view in hooks.get_hooks('register_admin_view')
                      if view.__name__ == 'page_edit']

        # 遍历页面视图并移除删除按钮
        for view in page_views:
            view.edit_handler.children.pop(delete_button_index)

remove_group_delete_button()
