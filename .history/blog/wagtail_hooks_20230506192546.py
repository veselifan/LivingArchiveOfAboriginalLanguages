from django.urls import reverse
from wagtail.admin.action_menu import ActionMenuItem
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks


@hooks.register("register_admin_menu_item")
def register_blog_menu_item():
    return MenuItem(
        "Blog",
        reverse("wagtailadmin_explore", args=("blog",)),
        classnames="icon icon-fa-pencil",
        order=1000,
    )


@hooks.register("register_admin_menu_item")
def register_add_blog_menu_item():
    return ActionMenuItem(
        "Add a new Blog",
        reverse("wagtailadmin_pages:add", args=("blog", "blogdetailpage", "{{ request.site.root_page.pk }}")),
        classnames="icon icon-fa-plus",
        order=1001,
        attrs={"title": "Add a new Blog"},
    )
