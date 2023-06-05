from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.forms import CheckboxSelectMultiple
from wagtail.admin.viewsets.model import ModelViewSet
from django.urls import re_path
from wagtail.users.forms import GroupForm
from wagtail.users.views.groups import GroupViewSet as WagtailGroupViewSet, EditView, CreateView, IndexView, DeleteView
from wagtail.users.views.users import Index


class MyGroupForm(GroupForm):

    class Meta:
        model = Group
        fields = (
            "name",
            "permissions",
        )
        widgets = {
            "permissions": CheckboxSelectMultiple(),
        }




class MyCreateView(CreateView):
    template_name = "create_group.html"

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        # Create an object now so that the permission panel forms have something to link them against
        self.object = Group()

        form = self.get_form()
        if form.is_valid():
            response = self.form_valid(form)
            return response
        else:
            return self.form_invalid(form)


class MyIndexView(IndexView):
    """"""

class MyDeleteView(DeleteView):
    """"""
    def delete_action(self):
        raise PermissionDenied()

class MyEditView(EditView):
    template_name = "edit_group.html"


class GroupViewSet(ModelViewSet):
    model = Group
    icon = "group"
    edit_view_class = MyEditView
    add_view_class = MyCreateView
    delete_view_class = MyDeleteView

    form_fields = ['name']

    @property
    def users_view(self):
        return Index.as_view()

    def get_urlpatterns(self):
        return super().get_urlpatterns() + [
            re_path(r"(\d+)/users/$", self.users_view, name="users"),
        ]


group_viewset = GroupViewSet("my-groups")  # defines /admin/person/ as the base URL