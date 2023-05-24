from django.urls import reverse
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    yield MenuItem(
        'Add New Post',
        reverse('wagtailadmin_pages:add', args=('blog', 'blogdetailpage', page.pk)),
        classnames='button button-small button-secondary',
        attrs={'title': 'Add a new post'},
    )
    
    # Add more buttons for other articles here
    # ...

