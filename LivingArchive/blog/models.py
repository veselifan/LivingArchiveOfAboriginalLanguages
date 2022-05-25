from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtailgmaps.edit_handlers import MapFieldPanel



class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    formatted_address = models.CharField(max_length=255, null=True)
    latlng_address = models.CharField(max_length=255, null=True)


    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        MapFieldPanel('formatted_address'),
        MapFieldPanel('latlng_address', latlng=True),
    ]