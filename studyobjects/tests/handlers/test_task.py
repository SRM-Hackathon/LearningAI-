from django.test import TestCase

from studyobjects.handlers import TaskHandler
from user.factory import TeamFactory, UserFactory, PlatformUserFactory, TeamMembershipFactory


class TaskTests(TestCase):

    def test_create(self):
        team = TeamFactory(identity="T1345")
        user = UserFactory()
        platform_user = PlatformUserFactory(user=user)
        TeamMembershipFactory(platform_user=platform_user, team=team)
        data = {
            "name": "work on geometry",
            "eta": {
                "amount": 5,
                "unit": 'h'
            }
        }
        TaskHandler(data, platform_user, "create")



    # formatted_task_name = slugify(self.response["name"])
    # eta = get_displaced_time_from_duration_entity(self.response["eta"])
    # team = self.user.team
    # user_environment = UserEnvironment.objects.get(user=self.user)
    # assessment = user_environment.assessment
    # tag = user_environment.tag
    # Task.objects.get_or_create(
    #     name=formatted_task_name,
    #     assessment=assessment,
    #     tag=tag,
    #     student=self.user,
    #     eta=eta
    # )
    # return True