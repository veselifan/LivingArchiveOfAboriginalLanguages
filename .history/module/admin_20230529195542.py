from django.contrib import admin


# Register your models here.
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group, Permission

# 创建一个自定义的 GroupAdmin 类
class CustomGroupAdmin(GroupAdmin):
    # 设置可编辑的字段
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Permissions', {'fields': ('permissions',)}),
    )
    # 设置只读的字段
    readonly_fields = ('name',)

# 注册自定义的 GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
