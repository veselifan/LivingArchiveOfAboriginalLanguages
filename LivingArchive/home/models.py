from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from LivingArchive.settings.dev import API_KEY
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
class HomePage(Page):
    body = RichTextField(blank=True)
    #get data from file dev.py and pass to interface
    api_key = API_KEY,
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
