from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from LivingArchive.settings.dev import API_KEY

class HomePage(Page):
    body = RichTextField(blank=True)
    api_key = API_KEY,
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
