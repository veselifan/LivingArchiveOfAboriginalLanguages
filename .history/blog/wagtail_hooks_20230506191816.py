from django.urls import reverse
from wagtail.core import hooks
from wagtail.admin.action_menu import ActionMenuItem

@hooks.register('register_page_listing_more_buttons')
def page_listing_more_buttons(page, page_perms, is_parent=False):
    if isinstance(page, BlogListingPage):
        buttons = []
        for i in range(1, 7):
            url = reverse('wagtailadmin_pages:add', args=('blog', 'blogdetailpage', page.pk))
            buttons.append(ActionMenuItem(f'Add Blog {i}', url + f'?position=last-child&intro=Intro {i}&body=Body {i}&date=2023-05-06'))
        buttons.append(ActionMenuItem('More', reverse('wagtailadmin_explore', args=('blog',))))
        return buttons
