from django.urls import reverse
from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

@hooks.register('register_admin_menu_item')
def register_blog_menu_item():
    # Add a new menu item under the "Pages" menu
    return MenuItem(
        'Blog',
        reverse('blog'),
        classnames='icon icon-blog',
        order=10000
    )

@hooks.register('construct_main_menu')
def hide_explorer_menu_item(request, menu_items):
    # Remove the "Explorer" menu item from the main menu
    menu_items[:] = [item for item in menu_items if item.name != 'explorer']

@hooks.register('construct_homepage_summary_items')
def add_new_article_cta(request, items):
    # Add a "Add new article" button to the homepage summary
    items.append({
        'url': reverse('wagtailadmin_pages:add', args=('blog',)),
        'icon': 'fa-plus',
        'label': 'Add new article',
        'help_text': 'Add a new article to the blog',
        'classname': 'button button-small button-secondary',
    })

@hooks.register('construct_page_listing_buttons')
def page_listing_more_buttons(page, page_perms, is_parent=False):
    # Add a "More" button to the page listing buttons
    if page.__class__.__name__ == 'BlogDetailPage':
        return [
            {
                'label': 'More',
                'url': page.get_url(),
                'classname': 'button button-small button-secondary',
                'title': 'View more articles'
            }
        ]
    else:
        return []
