from django.urls import reverse
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)
from wagtail.core import hooks

from .models import BlogDetailPage


class BlogDetailPageModelAdmin(ModelAdmin):
    model = BlogDetailPage
    menu_label = 'Blog Posts'
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'date', 'author')
    search_fields = ('title',)

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        custom_urls = [
            path(
                '<int:page_id>/add-another-post/',
                self.edit_view,
                name='add_another_post'
            ),
        ]
        return urls + custom_urls

    def edit_view(self, request, page_id=None, *args, **kwargs):
        parent_page = BlogDetailPage.objects.get(id=page_id).get_parent()

        if request.method == 'POST':
            form = BlogDetailPageForm(request.POST)

            if form.is_valid():
                new_post = BlogDetailPage(
                    title=form.cleaned_data['title'],
                    date=form.cleaned_data['date'],
                    intro=form.cleaned_data['intro'],
                    body=form.cleaned_data['body'],
                    image=form.cleaned_data['image'],
                    video=form.cleaned_data['video'],
                    address=form.cleaned_data['address'],
                )
                parent_page.add_child(instance=new_post)
                new_post.save_revision().publish()

                # Redirect back to the index page
                index_url = reverse('wagtailadmin_explore', args=('pages',))
                return redirect(index_url)

        else:
            form = BlogDetailPageForm()

        context = {
            'form': form,
            'page_id': page_id,
        }
        return render(request, 'admin/add_another_post.html', context)


@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    if isinstance(page, BlogDetailPage):
        yield {
            'url': reverse('wagtailadmin_pages:add_another_post', args=(page.id,)),
            'label': 'Add Another Post',
            'classname': 'add-another-post',
            'title': 'Add another post under this parent page',
        }

    if isinstance(page, BlogListingPage) and not is_parent:
        yield {
            'url': reverse('wagtailadmin_pages:add', args=('blog', 'blog_detail_page', page.id)),
            'label': 'Add New Post',
            'classname': 'add-blog-post',
            'title': 'Add a new blog post to this page',
        }

    if isinstance(page, BlogDetailPage) or isinstance(page, BlogListingPage):
        yield {
            'url': reverse('blog_listing'),
            'label': 'More',
            'classname': 'blog-more',
            'title': 'See more blog posts',
        }


modeladmin_register(BlogDetailPageModelAdmin)
