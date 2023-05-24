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
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock

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

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        ImageChooserPanel("image"),
        VideoChooserPanel('video'),
        FieldPanel('body', classname="full"),
        MapFieldPanel('address', latlng=True, zoom=4),
    ]

class RectangleBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(required=True, max_length=100)
    description = blocks.TextBlock(required=True, max_length=500)

    class Meta:
        template = 'yourapp/blocks/rectangle_block.html'
        icon = 'image'
        label = 'Rectangle'

# 定义自定义布局类型
class ThreeRectanglesLayout(blocks.StructBlock):
    rectangle1 = RectangleBlock()
    rectangle2 = RectangleBlock()
    rectangle3 = RectangleBlock()

    class Meta:
        template = 'yourapp/blocks/three_rectangles_layout.html'
        icon = 'image'
        label = 'Three Rectangles'

# 定义页面模型
class MyPage(Page):
    body = StreamField([
        ('three_rectangles', ThreeRectanglesLayout()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
