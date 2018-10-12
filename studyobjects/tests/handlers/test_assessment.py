from django.contrib.auth.models import Group
from django.test import TestCase

from constants import GROUP_ADMINS
from studyobjects.factory import CourseFactory
from studyobjects.factory import AssessmentFactory
from studyobjects.handlers.assessment import AssessmentHandler
from studyobjects.models import Assessment, Tag
from user.factory import PlatformUserFactory, TeamMembershipFactory
from user.factory import TeamFactory
from user.factory import UserFactory

class AssessmentHandlerTests(TestCase):

    def test_create_assessment_assert_assessment_creation(self):
        team = TeamFactory()
        user = UserFactory()
        platform_user = PlatformUserFactory(user=user)
        team_membership = TeamMembershipFactory(team=team, platform_user=platform_user)
        admin_group = Group.objects.create(name=GROUP_ADMINS)
        team_membership.groups.add(admin_group)
        team_membership.save()
        course_object = CourseFactory(team=team, instructor=team_membership, name='maths')
        Tag.objects.create(name='Trigonometry', course=course_object)
        Tag.objects.create(name='Arithmetic', course=course_object)
        intent_response_dict = {
            'course': 'maths',
            'datetime': '2019-10-06T10:00:00Z',
            'tags': ['Trigonometry', 'Arithmetic']
        }
        AssessmentHandler(intent_response_dict, team_membership, "create")
        name = intent_response_dict['course'] + '_' + intent_response_dict['datetime']
        self.assertTrue(Assessment.objects.filter(
            name=name,
            course=course_object
        ).exists())

    # def test_list_all_assessments(self):
    #     team = TeamFactory()
    #     user = UserFactory()
    #     platform_user = PlatformUserFactory(user=user)
    #     team_membership = TeamMembershipFactory(team=team, platform_user=platform_user)
    #     course_object = CourseFactory(team=team, instructor=team_membership, name='maths')
    #     date_time = '2019-10-06T10:00:00Z'
    #     assessment = AssessmentFactory(course=course_object, created_by=team_membership, scheduled_at=date_time)
    #     intent_response_dict = {
    #         'course': 'maths'
    #     }
    #     assessments = AssessmentHandler(intent_response_dict, team_membership, "list_assessments")
    #     print(assessments)
    #     print(Assessment.objects.get(
    #         course=course_object
    #     ))
    #     self.assertEqual(Assessment.objects.get(
    #         course=course_object
    #     ), assessments)



