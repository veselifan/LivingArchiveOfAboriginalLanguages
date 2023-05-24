from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from django.urls import reverse
from django.utils.html import format_html
from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.hooks import register_rich_text_features



class AdditionalBlog(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
        FieldPanel('date'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date',)

class AdditionalBlogAdmin(ModelAdmin):
    model = AdditionalBlog
    menu_label = 'Additional Blogs'
    menu_icon = 'pilcrow'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # not required
    exclude_from_explorer = False  # not required
    list_display = ('title', 'date')
    search_fields = ('title',)

modeladmin_register(AdditionalBlogAdmin)

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/custom_admin.css')
    )

@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script>',
        static('js/custom_admin.js')
    )

@hooks.register('construct_main_menu')
def add_additional_blog_menu(request, menu_items):
    menu_items.append(
        MenuItem(
            'Additional Blogs',
            reverse('wagtailadmin_modeladmin_additionalblog_index'),
            classnames='icon icon-blog',
            order=1000
        )
    )
