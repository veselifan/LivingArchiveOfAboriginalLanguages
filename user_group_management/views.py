from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from wagtail.admin import messages

from .forms import UserGroupForm, GroupProfileFrom
from .models import GroupProfile

User = get_user_model()


def group_list(request):
    if request.method == 'POST':
        form = GroupProfileFrom(request.POST)
        group_name = form.cleaned_data['group_name']
        if Group.objects.exists(name=group_name):
            raise ValidationError('Group exists')
        group = Group.objects.create(name=group_name)
        GroupProfile.objects.create(group=group)
        return redirect('group_list')
    else:
        form = UserGroupForm()
    return render(request, 'group_index.html',
                  {'form': form, 'groups': [i.group.name for i in GroupProfile.objects.all()]})


class GroupProfileListView(TemplateView):
    template_name = 'group_list.html'

    def get(self, request, *args, **kwargs):
        not_created_groups = Group.objects.exclude(name__in=[i.group.name for i in GroupProfile.objects.all()])
        for group in not_created_groups:
            GroupProfile.objects.create(group=group)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            context['groups'] = GroupProfile.objects.all()
        else:
            context['groups'] = GroupProfile.objects.filter(create_by=user)
        return context

    def post(self, request, *args, **kwargs):
        group_name = request.POST.get('group_name')
        if group_name:
            if Group.objects.filter(name=group_name).exists():
                messages.error(request, 'Group already exists')
            else:
                group = Group.objects.create(name=group_name)
                GroupProfile.objects.create(group=group, create_by=request.user)

        return redirect(reverse('group_list'))


class GroupMembersView(TemplateView):
    template_name = 'group_members.html'

    def get_queryset(self):
        group = get_object_or_404(Group, id=self.kwargs['group_id'])
        return group.user_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(Group, id=self.kwargs['group_id'])
        context['group'] = group
        context['members'] = group.user_set.all()
        context['users'] = User.objects.exclude(groups__id=group.id)  # Only users not in the group
        return context

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, id=self.kwargs['group_id'])
        user_ids = request.POST.getlist('users')
        users = User.objects.filter(id__in=user_ids)
        group.user_set.add(*users)
        return redirect(reverse('group_members', args=[group.id]))


class RemoveMemberView(View):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        group_id = self.kwargs.get('group_id')

        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, id=group_id)

        group.user_set.remove(user)
        messages.success(request, 'User removed from group successfully')

        return redirect('group_members', group_id=group_id)
