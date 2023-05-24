from django.urls import reverse
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from wagtail.core.models import Page
from wagtail.core.views import serve

# 自定义视图
def more_articles(request):
    # 获取 BlogListingPage 页面
    blog_listing_page = Page.objects.get(slug='blog')
    # 获取页面下的所有 BlogDetailPage 页面
    blog_detail_pages = blog_listing_page.get_children().live().type(BlogDetailPage)

    return serve(request, blog_listing_page, show_in_menus=True, blog_detail_pages=blog_detail_pages)

# 添加菜单项
@hooks.register('register_admin_menu_item')
def register_more_articles_menu_item():
    return MenuItem('More Articles', reverse('more_articles'), classnames='icon icon-folder-inverse', order=10000)

# 添加路由
@hooks.register('register_admin_urls')
def register_more_articles_url():
    return [
        path('more-articles/', more_articles, name='more_articles'),
    ]

class BlogListingPage(Page):
    # ...

    def get_latest_blog_detail_pages(self):
        return self.get_children().live().type(BlogDetailPage).order_by('-first_published_at')[:6]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['latest_blog_detail_pages'] = self.get_latest_blog_detail_pages()
        return context

{% extends "base.html" %}

{% block content %}
  {% for page in latest_blog_detail_pages %}
    <div class="blog-post">
      {% image page.image fill-300x200 %}
      <h2><a href="{{ page.url }}">{{ page.title }}</a></h2>
      <p>{{ page.intro }}</p>
    </div>
  {% endfor %}
  <a href="/admin/more-articles/" class="more-link">More</a>
{% endblock %}
