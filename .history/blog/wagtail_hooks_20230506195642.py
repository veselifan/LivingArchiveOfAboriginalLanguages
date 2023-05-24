from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.widgets import Button, ButtonWithDropdownFromHook, PageListingButton

from django.utils.html import format_html

from wagtail.core import hooks


class BlogListingPage(Page):
    """Listing page list all the blog detail pages"""
    template = "blog/blog_listing_page.html"
    """to limit only 1 home page"""
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().all().order_by('-first_published_at')
        return context


class BlogDetailPage(Page):
    """Blog detail page"""
    template = "blog/blog_detail_page.html"

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    video = models.ForeignKey('wagtailvideos.Video',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    email = models.CharField(max_length=255, null=True)

    address = models.CharField(max_length=255, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        ImageChooserPanel("image"),
        VideoChooserPanel('video'),
        FieldPanel('body', classname="full"),
        FieldPanel('email'),
        MapFieldPanel('address', latlng=True, zoom=4),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('slug'),
    ]

    # Here we use the `register_rich_text_features` hook to register a custom feature that inserts a
    # "More" button with a link to the next blog post.
    @classmethod
    def get_more_button(cls):
        def add_more_to_body(features):
            button = features.register_link_type(ButtonWithDropdownFromHook('Blog post', 'wagtailcore.page', classnames='richtext-editor__link', can_choose_root=False, filter_page_types=[cls]))
            cls.more_button_name = button.name
            return features

        return add_more_to_body

    @hooks.register('register_rich_text_features')
    def register_more_button(features):
        cls.get_more_button()(features)

    # Here we use the `register_page_listing_buttons` hook to add buttons to the page listing view
    @classmethod
    def get_page_listing_buttons(cls):
        def add_listing_buttons(page, page_perms, is_parent=False):
            listing_buttons = []

            # We only show the listing buttons on the BlogListingPage
            if isinstance(page.specific, cls):
                # We add the "More" button to the listing view as a drop-down item
                listing_buttons.append(
                    ButtonWithDropdownFromHook(
                        'More',
                        hook_name='get_more_blog_posts',
                        classes=['button-small', 'button-secondary'],
                        page=page,
                        dropdown_css_class='dropdown-right'
