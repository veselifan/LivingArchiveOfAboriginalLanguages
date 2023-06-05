from wagtail.admin.views.pages import EditView
from wagtail.core import hooks


@hooks.register('register_group_permission_panel')
def remove_group_delete_button():
    from wagtail.admin.edit_handlers import ObjectList

    group_name = 'test1'  # 替换为您要移除删除按钮的组名

    # 获取删除按钮的索引位置
    delete_button_index = None
    for i, handler in enumerate(EditView.base_form_edit_handler.children):
        if isinstance(handler, ObjectList):
            delete_button_index = i + 1
            break

    if delete_button_index is not None:
        # 重写 EditView 的 delete 方法，以禁用删除操作
        def delete(self, request, *args, **kwargs):
            return self.error_response(request, message="You do not have permission to delete this page.")

        # 移除删除按钮
        EditView.base_form_edit_handler.children.pop(delete_button_index)

        # 获取所有注册的页面视图
        page_views = [view for view in hooks.get_hooks('register_admin_view')
                      if issubclass(view, EditView)]

        # 遍历页面视图并替换 delete 方法
        for view in page_views:
            setattr(view, 'delete', delete)

remove_group_delete_button()
