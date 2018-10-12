from django.test import TestCase

from constants import GROUP_COURSE_INSTRUCTORS
from studyobjects.handlers.assessment import create_assessment
from user.factory import PlatformUserFactory, TeamMembershipFactory
from user.factory import TeamFactory
from user.factory import UserFactory


# def create_assessment(parameter_dict, team_membership):
#     course = parameter_dict['course'].string_value
#     name = parameter_dict['name'].string_value
#     list_tags = parameter_dict['tags'].list_value.values
#     tags = []
#     for item in list_tags:
#         tags.append(item.string_value)
#     datetime = parameter_dict['datetime'].struct_value.fields['date_time'].string_value
#     Assessment.objects.create(
#         course=course,
#         name=name,
#         tags=tags,
#         scheduled_at=datetime,
#         created_by=team_membership
#     )
#     print(parameter_dict)

