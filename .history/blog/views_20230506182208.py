from django.shortcuts import render
from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import render

class LinkPage(Page):
    pass

def link_page(request):
    return render(request, "link_page.html", {
        'page': LinkPage(),
    })

# Create your views here.


