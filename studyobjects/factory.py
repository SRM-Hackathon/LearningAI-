from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from studyobjects.models import Course
from user.factory import TeamMembershipFactory, TeamFactory


class CourseFactory(DjangoModelFactory):

    class Meta:
        model = Course

    name = FuzzyText()


    instructor = SubFactory(TeamMembershipFactory)
    team =SubFactory(TeamFactory)
