from django.contrib import admin


# Register your models here.
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

# 创建一个自定义的 GroupAdmin 类
class CustomGroupAdmin(GroupAdmin):
    def has_add_permission(self, request):
        # 禁用创建组的功能
        return False

    def has_change_permission(self, request, obj=None):
        # 禁用编辑组的功能
        return False

# 注册自定义的 GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

