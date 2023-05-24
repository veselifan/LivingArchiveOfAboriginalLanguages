from django.db import models
#from mirage import fields
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtailgmaps.edit_handlers import MapFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from djangokeys import DjangoKeys
from django.contrib.auth.models import User
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import StructBlock, CharBlock
from wagtail.documents.blocks import DocumentChooserBlock

keys=DjangoKeys ("./livingarchive/settings/.env")

class BlogListingPage (Page):
    """Listing page list all the blog detail pages"""
    template = "blog/blog_listing_page.html"
    """to limit only 1 home page"""
    max_count = 1
    #get google maps api key from .env
    api_key = keys.str("API_KEY")
    #to get detail from blog detail page
    
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().all().order_by('-first_published_at')

        return context

class LinkBlock(StructBlock):
    title = CharBlock(required=True, help_text="Enter the link title")

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
     # Return a hiding version of self.email
     
    email=User(Page.owner).email.replace("@"," at " )
    
    address = models.CharField(max_length=255, null=True)

    links = StreamField([
        ('link', LinkBlock()),
    ], blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        ImageChooserPanel("image"),
        VideoChooserPanel('video'),
        FieldPanel('body', classname="full"),
        MapFieldPanel('address', latlng=True, zoom=4),
        StreamFieldPanel('links'),
    ]