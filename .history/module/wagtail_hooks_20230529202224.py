from wagtail.admin.views.pages import PageViewSet
from wagtail.core import hooks


@hooks.register('register_group_permission_panel')
def remove_group_delete_button():
    from wagtail.admin.views.pages import PAGE_EDIT_HANDLERS
    from wagtail.admin.edit_handlers import ObjectList

    group_name = 'test1'  # 替换为您要移除删除按钮的组名

    # 获取删除按钮的索引位置
    delete_button_index = None
    for i, handler in enumerate(PAGE_EDIT_HANDLERS):
        if isinstance(handler, ObjectList):
            delete_button_index = i + 1
            break

    if delete_button_index is not None:
        # 重写页面视图集的 delete 方法，以禁用删除操作
        def delete(self, request, *args, **kwargs):
            return self.error_response(request, message="You do not have permission to delete this page.")

        # 移除删除按钮
        PAGE_EDIT_HANDLERS.pop(delete_button_index)

        # 获取所有注册的页面视图集
        page_viewsets = [viewset for viewset in hooks.get_hooks('register_admin_viewset')
                         if issubclass(viewset.cls, PageViewSet)]
        
        # 遍历页面视图集并替换 delete 方法
        for viewset in page_viewsets:
            if viewset.permission_policy.permission_policy_class.get_permission_policy().get_change_permission_string(None):
                setattr(viewset.cls, 'delete', delete)

remove_group_delete_button()
