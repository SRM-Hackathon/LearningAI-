from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from user.models import PlatformUser
from user.models import Team
from user.models import TeamMembership
from user.models import User


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    username = FuzzyText()


class PlatformUserFactory(DjangoModelFactory):

    class Meta:
        model = PlatformUser

    identity = FuzzyText()

    user = SubFactory(User)


class TeamFactory(DjangoModelFactory):

    class Meta:
        model = Team

    identity = FuzzyText()
    name = FuzzyText()
    access_token = FuzzyText()


class TeamMembershipFactory(DjangoModelFactory):

    class Meta:
        model = TeamMembership

    platform_user = SubFactory(PlatformUserFactory)
    team = SubFactory(TeamFactory)
