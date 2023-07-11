from django.urls import path
from .views import GroupMembersView, RemoveMemberView

app_name = 'user_group_management'
urlpatterns = [
    path('group/<int:group_id>/', GroupMembersView.as_view(), name='group_members'),
]
