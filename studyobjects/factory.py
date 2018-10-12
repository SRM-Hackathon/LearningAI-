from django.utils import timezone
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyDateTime

from studyobjects.models import Course, UserEnvironment, Tag, Assessment
from user.factory import TeamMembershipFactory, TeamFactory
from studyobjects.models import Task

from django.utils import timezone

class CourseFactory(DjangoModelFactory):

    class Meta:
        model = Course

    name = FuzzyText()

    instructor = SubFactory(TeamMembershipFactory)
    team = SubFactory(TeamFactory)


class TagFactory(DjangoModelFactory):

    class Meta:
        model = Tag
    name = FuzzyText()
    description = FuzzyText()

    course = SubFactory(CourseFactory)


class AssessmentFactory(DjangoModelFactory):

    class Meta:
        model = Assessment

    name = FuzzyText()
    description = FuzzyText()
    scheduled_at = FuzzyDateTime(start_dt=timezone.now())

    course = SubFactory(CourseFactory)
    created_by = SubFactory(TeamMembershipFactory)


class UserEnvironmentFactory(DjangoModelFactory):

    class Meta:
        model = UserEnvironment

    user = SubFactory(TeamMembershipFactory)
    assessment = SubFactory(AssessmentFactory)
    tag = SubFactory(TagFactory)


class TaskFactory(DjangoModelFactory):

    class Meta:
        model = Task

    name = FuzzyText()
    assessment = SubFactory(AssessmentFactory)
    description = "Some dummy task"
    student = SubFactory(TeamMembershipFactory)
    tag = SubFactory(TagFactory)

