from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

@hooks.register('register_page_listing_buttons')
def add_new_blog_listing_button(page, page_perms, is_parent=False):
    """
    This adds a button on BlogListingPage to create a new BlogDetailPage.
    """
    if isinstance(page, BlogListingPage):
        url = reverse('wagtailadmin_pages:add', args=('blog', 'blogdetailpage', page.id,))
        return [
            MenuItem('Add new blog post', url, classnames='icon icon-new'),
        ]
