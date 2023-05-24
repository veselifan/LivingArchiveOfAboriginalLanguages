from django.urls import reverse
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

@hooks.register('construct_main_menu')
def add_blog_menu_item(request, menu_items):
    # Create a sub-menu item for blog posts
    blog_posts_menu_item = MenuItem(
        'Blog Posts',
        reverse('blog_listing_page'),
        classnames='icon icon-blog',
        order=1000
    )

    # Add the sub-menu item after the Pages menu item
    menu_items.insert(1, blog_posts_menu_item)

    # Create sub-menu items for each blog post
    for i in range(1, 7):
        post_menu_item = MenuItem(
            f'Blog Post {i}',
            reverse('blog_detail_page', args=(i,)),
            classnames='icon icon-document',
            order=blog_posts_menu_item.order + i
        )

        # Add the sub-menu item to the Blog Posts sub-menu
        blog_posts_menu_item.submenu_items.append(post_menu_item)

    # Add a "More" link to the Blog Posts sub-menu
    more_menu_item = MenuItem(
        'More...',
        '#',
        classnames='icon icon-arrow-down',
        order=blog_posts_menu_item.order + 7
    )

    # Add the "More" link to the Blog Posts sub-menu
    blog_posts_menu_item.submenu_items.append(more_menu_item)

    # Create sub-menu items for each additional blog post
    for i in range(7, 11):
        post_menu_item = MenuItem(
            f'Blog Post {i}',
            reverse('blog_detail_page', args=(i,)),
            classnames='icon icon-document',
            order=more_menu_item.order + i - 7
        )

        # Add the sub-menu item to the "More" sub-menu
        more_menu_item.submenu_items.append(post_menu_item)
