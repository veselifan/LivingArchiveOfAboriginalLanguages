from wagtail.core import hooks
from django.urls import reverse
from wagtail.admin.menu import MenuItem
from wagtail.admin.action_menu import ActionMenuItem

@hooks.register('register_page_listing_more_buttons')
def page_listing_more_buttons(page, page_perms, is_parent=False):
    if isinstance(page, BlogListingPage):
        url = reverse('wagtailadmin_pages:add', args=('blog', 'blogdetailpage', page.id,))
        return [
            ActionMenuItem('Add Blog Post', url, icon='add'),
        ]
    return []

@hooks.register('register_admin_menu_item')
def register_blog_menu_item():
    return MenuItem('Blog', reverse('wagtailadmin_explore', args=['blog']), classnames='icon icon-blog', order=300)

