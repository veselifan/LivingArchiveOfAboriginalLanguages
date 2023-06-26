from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class UserGroupForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    group = forms.ModelChoiceField(queryset=Group.objects.all())


class GroupProfileFrom(forms.Form):
    group_name = forms.CharField(max_length=256, required=True)
