from wagtail.core import hooks
from django.urls import reverse
from wagtail.admin.menu import MenuItem

# Define a hook to add the "Add new blog post" button
@hooks.register('register_page_listing_buttons')
def add_new_blog_post_button(page, page_perms, is_parent=False):
    if isinstance(page, BlogListingPage):
        url = reverse('wagtailadmin_pages:add', args=('blog',))
        return [
            {
                'label': 'Add new blog post',
                'url': url,
                'classname': 'button button-small button-secondary',
                'title': 'Add a new blog post under {}'.format(page.get_admin_display_title()),
                'permissions': page_perms,
            }
        ]

# Define a hook to add the "More" button to each blog post
@hooks.register('insert_editor_js')
def add_more_button():
    return """
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                var moreLinks = document.querySelectorAll(".more-link");
                moreLinks.forEach(function(link) {
                    var moreButton = document.createElement("a");
                    moreButton.innerText = "More";
                    moreButton.href = link.href;
                    moreButton.className = "button";
                    link.parentElement.appendChild(moreButton);
                });
            });
        </script>
    """

# Define a hook to add the image and link blocks to the blog detail page
@hooks.register('register_block_types')
def register_custom_blocks():
    return [
        ('image_link', ImageLinkBlock()),
    ]

# Define a custom block for the image and link combination
class ImageLinkBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    link = blocks.URLBlock()

    class Meta:
        icon = 'image'
        template = 'blocks/image_link_block.html'

# Define the template for the image and link block
{% extends "blocks/base_block.html" %}

{% block content %}
    <div class="image-link-block">
        <a href="{{ value.link }}"><img src="{{ value.image.url }}" alt="{{ value.image.alt }}"></a>
    </div>
{% endblock %}

# Define a hook to add the image and link blocks to the blog detail page content panels
@hooks.register('construct_page_editor_js')
def add_image_link_blocks():
    return """
        function BlogDetailPageBlockHandler(blockDef, block){
            if (blockDef.name === "image_link") {
                var image = blockDef.meta_options.image;
                var link = blockDef.meta_options.link;
                return {
                    id: block.id,
                    type: 'image_link',
                    value: {
                        image: {
                            id: image.id,
                            title: image.title,
                            alt: image.alt,
                            url: image.url
                        },
                        link: link.value
                    }
                };
            }
        }
        registerBlockHandler('image_link', BlogDetailPageBlockHandler);
    """

# Define a hook to add the image and link blocks to the blog detail page content panels
@hooks.register('construct_page_editor_js')
def add_image_link_panel():
    return """
        function BlogDetailPagePanel() {
            return [
                imageChooserPanel({
                    name: 'image',
                    required: false
                }),
                fieldPanel({
                    name: 'link',
                    label: 'Link',
                    widget: forms.URLInput
                })
            ];
        }
        registerPanelBlock('image_link', BlogDetailPagePanel);
    """

# Define a hook to add the image and link blocks to the blog detail page content panels
BlogDetailPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('intro'),
    ImageChooser
    
    
class BlogDetailPageCarouselItem(models.Model):
    page = ParentalKey(
        'BlogDetailPage',
        related_name='carousel_items'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    link_url = models.URLField()

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('link_url'),
    ]
