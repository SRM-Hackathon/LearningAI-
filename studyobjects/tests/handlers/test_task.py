from django.test import TestCase

from studyobjects.factory import UserEnvironmentFactory, CourseFactory, AssessmentFactory, TagFactory
from studyobjects.handlers import TaskHandler
from user.factory import TeamFactory, UserFactory, PlatformUserFactory, TeamMembershipFactory
from studyobjects.factory import TaskFactory


class TaskTests(TestCase):

    def test_create(self):
        team = TeamFactory(identity="T1345")
        user = UserFactory()
        platform_user = PlatformUserFactory(user=user)
        tm = TeamMembershipFactory(platform_user=platform_user, team=team)
        data = {
            "name": "work on geometry",
            "eta": {
                "amount": 5,
                "unit": 'h'
            }
        }
        team = TeamFactory()
        course = CourseFactory(team=team, instructor=tm)
        assessment = AssessmentFactory(course=course, created_by=tm)
        tag = TagFactory(course=course)
        UserEnvironmentFactory(user=tm, tag=tag, assessment=assessment)
        TaskHandler(data, tm, "create")

    def test_upgrade(self):
        task_name = "practise-examples"
        team = TeamFactory(identity="T1345")
        user = UserFactory()
        platform_user = PlatformUserFactory(user=user)
        tm = TeamMembershipFactory(platform_user=platform_user, team=team)
        course = CourseFactory(team=team, instructor=tm)
        tag = TagFactory(course=course)
        assessment = AssessmentFactory(course=course, created_by=tm)
        tag = TagFactory(course=course)
        UserEnvironmentFactory(user=tm, tag=tag, assessment=assessment)
        task = TaskFactory(name=task_name, assessment=assessment, student=tm, tag=tag)
        data = {'task': task_name}
        TaskHandler(data, tm, "upgrade_state")
