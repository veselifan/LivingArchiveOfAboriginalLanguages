# Create your models here.
from django.contrib.auth.models import Group, User
from django.db import models


class GroupProfile(models.Model):
    create_by = models.ForeignKey(User, verbose_name='created_by', related_name='group_profiles', null=True,
                                  on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, verbose_name='group', on_delete=models.CASCADE, related_name='group_profile')
