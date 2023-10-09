import os
import re
from datetime import datetime

import requests
from django.contrib.auth.models import User
from django.db import models
from django.template.response import TemplateResponse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import StructBlock, CharBlock
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField

# from mirage import fields
from wagtail.core.models import Page
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import PAGE_TEMPLATE_VAR
from wagtail_pdf_view.mixins import PdfViewPageMixin
from wagtailgmaps.edit_handlers import MapFieldPanel
from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel

from dotenv import load_dotenv
load_dotenv()
api_key=str(os.getenv("API_KEY"))

class BlogListingPage(Page):
    """Listing page list all the blog detail pages"""

    template = "blog/blog_listing_page.html"
    """to limit only 1 home page"""
    max_count = 6

    # get google maps api key from .env

    # to get detail from blog detail page

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = (
            BlogDetailPage.objects.live().all().order_by("-first_published_at")
        )
        print('-----')
        print(context["posts"])
        return context


class LinkBlock(StructBlock):
    title = CharBlock(required=True, help_text="Enter the link title")
    url = CharBlock(required=True, help_text="Enter the link URL")
    document = DocumentChooserBlock(
        required=False, help_text="Choose a document for this link"
    )


class BlogDetailPage(Page, PdfViewPageMixin):
    """Blog detail page"""

    # base_form_class = CustomPageForm
    # edit_handler = CustomEditView

    ROUTE_CONFIG = [
        ("html", r'^$'),
        ("pdf", r'^pdf/$'),
    ]

    template = "blog/blog_detail_page.html"
    date = models.PositiveIntegerField("Post date", choices=[
        (year, year) for year in range(1970, datetime.now().year+1)
    ], default=1970, null=True, blank=True)
    intro = models.CharField(max_length=250, null=True, blank=True)
    body = RichTextField(null=True, blank=True)

    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    video = models.ForeignKey(
        "wagtailvideos.Video",
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    # Return a hiding version of self.email

    email = User(Page.owner).email.replace("@", " at ")

    address = models.CharField(max_length=255, null=True, blank=True)

    # hidden field, not show, for backup
    address_backup = models.CharField(max_length=255, null=True, blank=True)

    # location = models.CharField(max_length=255, null=True, blank=True)
    audio = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    language = models.CharField(max_length=255, null=True, blank=True)

    links = StreamField(
        [
            ("link", LinkBlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("language"),
        # FieldPanel("location"),
        ImageChooserPanel("image"),
        VideoChooserPanel("video"),
        MediaChooserPanel("audio"),
        FieldPanel("body", classname="full"),
        DocumentChooserPanel("pdf"),
        MapFieldPanel("address", latlng=True, zoom=4),
        StreamFieldPanel("links"),
    ]

    # def get_template(self, request, *args, **kwargs):
    #     tester = self.permissions_for_user(request.user)
    #     # if self.permissions_for_user(request.user):
    #     #     return 'blog/password_required.html'
    #     # 检查用户是否有查看权限
    #     # print(self.get_view_restrictions())
    #     # can_view = permissions.can_view()
    #     # blog_post = self.specific
    #     # print(blog_post.serve(request))
    #     # return blog_post.serve(request)
    #     # print(BlogDetailPage.objects.private())
    #     return self.template

    def get_context(self, request, *args, **kwargs):
        context = {
            PAGE_TEMPLATE_VAR: self,
            "self": self,
            "request": request,
        }

        if self.context_object_name:
            context[self.context_object_name] = self

        context["accept"] = kwargs["accept"] if "accept" in kwargs else True
        return context

    def serve(self, request, *args, **kwargs):
        if "accept" not in kwargs:
            kwargs["accept"] = True
        request.is_preview = False

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            self.get_context(request, *args, **kwargs),
        )

    def get_password_restriction(self):
        return self.get_view_restrictions().filter(restriction_type="password").first()


def address2latlng(address):
    """Get latlng from google map api"""
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url, timeout=5)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        print(f'lat：{longitude}, long：{latitude}')
        return ','.join([str(latitude), str(longitude)])
    return ''


@receiver(pre_save, sender=BlogDetailPage)
def blog_details_pre_save(sender, instance, **kwargs):
    pattern = r'^-?\d+\.\d+,-?\d+\.\d+$'
    if not re.match(pattern, instance.address):
        # if is not a valid latlng, get latlng from google map api
        instance.address_backup = instance.address
        instance.address = address2latlng(instance.address)
