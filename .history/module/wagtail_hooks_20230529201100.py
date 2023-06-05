from django.urls import reverse
from wagtail.contrib.modeladmin.views import IndexView
from django.contrib.auth.models import GroupManager
from django.http import HttpResponseForbidden

class CustomGroupEditView(IndexView):
    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            group_id = kwargs.get('instance_id')
            group = Group.objects.filter(id=group_id).first()
            if group and group.name == 'test1':
                return HttpResponseForbidden('You are not allowed to delete this group.')

        return super().post(request, *args, **kwargs)

    def get_edit_url(self, instance):
        if instance.name == 'test1':
            return reverse('wagtailusers_groups')

        return super().get_edit_url(instance)

custom_group_edit_view = CustomGroupEditView()
