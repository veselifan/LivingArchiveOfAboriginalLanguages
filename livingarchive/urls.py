from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from user_group_management.views import GroupProfileListView, GroupMembersView, RemoveMemberView

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('group/', GroupProfileListView.as_view(), name='group_list'),
    path('group/<int:group_id>/', GroupMembersView.as_view(), name='group_members'),
    path('group/<int:group_id>/remove_member/<int:user_id>/', RemoveMemberView.as_view(), name='remove_member'),
    path('documents/', include(wagtaildocs_urls)),
    path('search/', search_views.search, name='search'),
    path(r'', include('allauth.urls')),
    path(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
