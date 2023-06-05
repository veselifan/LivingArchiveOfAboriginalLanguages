from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.users.models import Group
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def group_view(request):
    user_groups = Group.objects.filter(user=request.user)
    # 进行适当的查询以获取用户所属的小组列表
    # ...
    # 根据需要进行其他逻辑处理
    return HttpResponse("User's groups: {}".format(user_groups))

@hooks.register('construct_main_menu')
def add_custom_menu_item(request, menu_items):
    menu_items.append(
        MenuItem('Groups', reverse('group_view'), classnames='icon icon-group', order=1000)
    )
