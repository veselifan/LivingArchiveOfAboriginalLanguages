from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from djangokeys import DjangoKeys
keys=DjangoKeys ("./LivingArchive/settings/.env")


import logging
logger = logging.getLogger(__name__)

class HomePage(Page):
    
    body = RichTextField(blank=True)
    #get data from file dev.py and pass to interface
    api_key = keys.str("API_KEY")
    #logging.warn("Api_Key", API_KEY,)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
