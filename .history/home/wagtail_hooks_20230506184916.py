from django.urls import reverse
from wagtail.core import hooks


@hooks.register('register_page_listing_buttons')
def page_listing_button(page, page_perms, is_parent=False):
    if page.__class__.__name__ == 'BlogListingPage':
        yield {
            'url': reverse('admin:blog_blogdetailpage_add'),
            'label': 'Add New Article',
            'class': 'button button-small',
        }

    if page.__class__.__name__ == 'BlogDetailPage':
        return None

    if page.__class__.__name__ == 'BlogListingPage':
        yield {
            'url': reverse('admin:blog_bloglistingpage'),
            'label': 'More...',
            'class': 'button button-small button-secondary',
        }
<!DOCTYPE html>
<html>
<head>
    <title>Map Marker</title>
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&libraries=places"></script>
</head>
<body>
    <div id="map" style="height: 400px; width: 100%;"></div>

    <script>
        // Your JavaScript code will go here
    </script>
</body>
</html>
