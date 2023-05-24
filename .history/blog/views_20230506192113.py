from django.shortcuts import render
from django.views.generic import DetailView
from .models import BlogPage

class BlogPageDetailView(DetailView):
    model = BlogPage
    template_name = 'blog/blog_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blog_pages = BlogPage.objects.all()
        context['blog_pages'] = blog_pages

        return context
