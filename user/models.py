from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import JSONField

from mixins import TimeStampMixin


class Team(TimeStampMixin):

    identity = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=80, null=True)
    access_token = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.name}"


class PlatformUser(TimeStampMixin):

    identity = models.CharField(max_length=20, primary_key=True)
    channel_id = models.CharField(null=True, max_length=20)
    data = JSONField(null=True)

    teams = models.ManyToManyField(
        Team,
        related_name="platform_users",
        through="TeamMembership"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TeamMembership(TimeStampMixin):

    platform_user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, related_name="team_memberships")

    class Meta:
        unique_together = ('platform_user', 'team')
