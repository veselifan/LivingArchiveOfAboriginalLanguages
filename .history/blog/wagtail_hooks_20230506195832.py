from wagtail.core import hooks
from django.urls import reverse
from django.utils.html import format_html

@hooks.register('construct_page_listing_buttons')
def add_blog_button(page, page_type, context, *args, **kwargs):
    if page_type == 'blog.BlogListingPage':
        # Get the URL of the add page view for BlogDetailPage
        add_blog_url = reverse('wagtailadmin_pages:add', args=('blog', 'blogdetailpage', page.pk))

        # Generate the button HTML and return it
        button_html = """
            <a href="{add_blog_url}" class="button button-small">
                Add Blog
            </a>
        """.format(add_blog_url=add_blog_url)

        return format_html(button_html)