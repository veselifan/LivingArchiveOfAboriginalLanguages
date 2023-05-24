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
from wagtail.core import blocks


keys=DjangoKeys ("./livingarchive/settings/.env")


#新增代码
class LinkPage(Page):
    """Page for external links"""
    template = "blog/link_page.html"

    link = models.URLField()

    content_panels = Page.content_panels + [
        FieldPanel('link'),
    ]
    
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
        #新增代码
        context["links"] = LinkPage.objects.live().all()
        context["articles"] = self.articles

        return context

#新增代码
class LinkBlock(StructBlock):
    title = CharBlock(required=True, help_text="Enter the link title")
    url = CharBlock(required=True, help_text="Enter the link URL")
    document = DocumentChooserBlock(required=False, help_text="Choose a document for this link")

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

    #新增代码
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
        #新增代码
        StreamFieldPanel('links'),
    ]


class FeaturedArticle(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content = models.TextField()

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('content', classname="full")
    ]

    def __str__(self):
        return self.title
    
class BlogListingPage(Page):
    # ...
    featured_articles = StreamField([
        ('featured_article', blocks.StructBlock([
            ('title', blocks.CharBlock(required=True)),
            ('image', blocks.StructBlock([
                ('image', blocks.ImageChooserBlock(required=True)),
                ('caption', blocks.CharBlock(required=False)),
            ], required=True)),
            ('content', blocks.RichTextBlock(required=True)),
        ], icon='doc-full-inverse'))
    ], blank=True)

    content_panels = Page.content_panels + [
        # ...
        StreamFieldPanel('featured_articles')
    ]

{% extends "base.html" %}

{% block content %}
    <h1>{{ page.title }}</h1>
    <ul>
        {% for post in posts %}
            <li><a href="{{ post.url }}">{{ post.title }}</a></li>
        {% endfor %}
    </ul>
    {% if more %}
        <a href="{{ more.url }}" class="more-link">{{ more.title }}</a>
    {% endif %}
{% endblock %}

