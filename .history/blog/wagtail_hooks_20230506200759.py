from django.urls import reverse
from wagtail.core import hooks

@hooks.register('insert_editor_js')
def editor_js():
    return '<script src="{0}"></script>'.format(reverse('core:static', args=['js/editor.js']))

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return '<link rel="stylesheet" href="{0}" />'.format(reverse('core:static', args=['css/admin.css']))

@hooks.register('construct_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    yield {
        'url': reverse('add_another_article', args=[page.id]),
        'label': 'Add Another Article',
        'classname': 'icon icon-add',
        'title': 'Add another article',
    }

@hooks.register('before_serve_page')
def add_another_article(request, page):
    if request.resolver_match.url_name == 'add_another_article':
        parent_page = page.get_parent()
        article = BlogDetailPage(title="New Article", parent=parent_page)
        article.save()
        return redirect(article.url)
