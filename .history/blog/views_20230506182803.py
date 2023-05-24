from django.shortcuts import render
from django.shortcuts import render
from blog.models import Link_Page

def link_page(request):
    link_page = LinkPage.objects.first()
    return render(request, 'blog/link_page.html', {
        'link_page': link_page
    })

def home_page(request):
    return render(request, 'home_page.html')

