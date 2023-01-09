from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import Group


class LocalSignupForm(forms.Form):
    pass

    def signup(self, request, user):
        role = request.session.get('user_type')
        group = role or "Contributors"
        g = Group.objects.get(name=group)
        user.groups.add(g)
        user.save()
