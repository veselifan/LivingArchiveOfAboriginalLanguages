import os

from captcha.fields import CaptchaField
from django.db import models
from dotenv import load_dotenv
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtailcaptcha.models import WagtailCaptchaEmailForm

from blog.models import BlogDetailPage

# from wagtail.core import blocks
# from wagtailstreamforms.fields import BaseField, register
# get google maps api key from .env
load_dotenv()

api_key = str(os.getenv("API_KEY"))


# @register('recaptcha')
class HomePage(WagtailCaptchaEmailForm, Page):
    """Home Page model"""

    templates = "home/home_page.html"

    """to limit only 1 home page"""
    max_count = 1
    captcha = CaptchaField()

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    landing_page_template = "home/home_page_landing.html"

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
    ]

    # to get detail from blog detail page
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = (
            BlogDetailPage.objects.live().all().order_by("-first_published_at")
        )
        return context

    """set verbose name"""

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


class FormField(AbstractFormField):
    page = ParentalKey(
        "HomePage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )
