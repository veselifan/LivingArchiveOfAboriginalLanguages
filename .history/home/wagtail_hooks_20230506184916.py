from django.urls import reverse
from wagtail.core import hooks


@hooks.register('register_page_listing_buttons')
def page_listing_button(page, page_perms, is_parent=False):
    if page.__class__.__name__ == 'BlogListingPage':
        yield {
            'url': reverse('admin:blog_blogdetailpage_add'),
            'label': 'Add New Article',
            'class': 'button button-small',
        }

    if page.__class__.__name__ == 'BlogDetailPage':
        return None

    if page.__class__.__name__ == 'BlogListingPage':
        yield {
            'url': reverse('admin:blog_bloglistingpage'),
            'label': 'More...',
            'class': 'button button-small button-secondary',
        }
