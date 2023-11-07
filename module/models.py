import os
from django.db import models
#from mirage import fields
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtailgmaps.edit_handlers import MapFieldPanel
#from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from dotenv import load_dotenv
load_dotenv()
#get google maps api key from .env
api_key=str(os.getenv("API_KEY"))

class ModuleListingPage (Page):
    """Listing page list all the module detail pages"""
    template = "module/module_listing_page.html"
    """to limit only 1 home page"""
    max_count = 1
    #to get detail from module detail page
    
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        # Build a menu from live pages that are children of the homepage
        context["menu_items"] = homepage.get_children().live().in_menu()

        context["posts"] = ModuleDetailPage.objects.live().all().order_by('-last_published_at')

        return context
    
class ModuleDetailPage(Page):
    """Module detail page"""
    template = "module/module_detail_page.html"
    
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
    

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
       # ImageChooserPanel("image"),
        VideoChooserPanel('video'),
        FieldPanel('body', classname="full"),
    ]


