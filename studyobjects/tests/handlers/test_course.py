from django.contrib.auth.models import Group
from django.test import TestCase

from constants import GROUP_ADMINS, GROUP_COURSE_INSTRUCTORS
from studyobjects.handlers.course import CourseHandler
from studyobjects.models import Course
from user.factory import PlatformUserFactory, TeamMembershipFactory
from user.factory import TeamFactory
from user.factory import UserFactory
from user.models import TeamMembership


class CourseHandlerTests(TestCase):

    def test_create_course_assert_course_creation(self):
        team = TeamFactory()
        admin = UserFactory()
        instructor = UserFactory()
        admin_platform_user = PlatformUserFactory(user=admin)
        instructor_platform_user = PlatformUserFactory(user=instructor)
        admin_group = Group.objects.create(name=GROUP_ADMINS)
        admin_membership = TeamMembershipFactory(team=team, platform_user=admin_platform_user)
        admin_membership.groups.add(admin_group)
        admin_membership.save()
        instructor_membership = TeamMembershipFactory(team=team, platform_user=instructor_platform_user)
        intent_response_dict = {
            "course": "maths",
            "instructor": instructor_platform_user.identity
        }
        CourseHandler(intent_response_dict, admin_membership, "create")
        self.assertTrue(Course.objects.filter(
            team=team,
            instructor=instructor_membership,
            name="maths"
        ).exists())

    # def test_create_course_assert_instructor_added_to_group(self):
    #     team = TeamFactory()
    #     admin = UserFactory()
    #     instructor = UserFactory()
    #     admin_platform_user = PlatformUserFactory(user=admin)
    #     instructor_platform_user = PlatformUserFactory(user=instructor)
    #     admin_group = Group.objects.create(name=GROUP_ADMINS)
    #     admin_membership = TeamMembershipFactory(team=team, platform_user=admin_platform_user)
    #     admin_membership.groups.add(admin_group)
    #     admin_membership.save()
    #     TeamMembershipFactory(team=team, platform_user=instructor_platform_user)
    #     intent_response_dict = {
    #         "course": "maths",
    #         "instructor": instructor_platform_user.identity
    #     }
    #     create_course(intent_response_dict, admin_membership)
    #     instructor_membership = TeamMembership.objects.get(platform_user=instructor_platform_user, team=team)
    #     self.assertTrue(
    #         instructor_membership.groups.filter(name=GROUP_COURSE_INSTRUCTORS).exists()
    #     )
