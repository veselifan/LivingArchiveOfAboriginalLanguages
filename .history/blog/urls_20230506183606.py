from django.urls import path
from blog.models import views

urlpatterns = [
    # ...
    path('links/<slug:slug>/', views.LinkPage.as_view(), name='link_page'),
]
