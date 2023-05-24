from wagtail.core import hooks

@hooks.register('insert_global_admin_css')
def global_admin_css():
    """
    Inject some custom CSS into the admin interface.
    """
    return '<link rel="stylesheet" href="{% static "css/custom.css" %}">'

@hooks.register('insert_editor_js')
def editor_js():
    """
    Add some custom JavaScript to the page editor.
    """
    return '<script src="{% static "js/custom.js" %}"></script>'

@hooks.register('construct_page_listing_buttons')
def add_view_another_article_button(page, page_perms, is_parent=False, next_url=None):
    """
    Add a button to the bottom of the page editor that links to another article.
    """
    if isinstance(page, BlogDetailPage):
        next_page = BlogDetailPage.objects.filter(date__lt=page.date).order_by('-date').first()
        if next_page:
            yield {
                'url': next_page.url,
                'label': 'View Next Article',
                'class': 'button button-small',
                'title': 'View the next article in this blog',
            }
