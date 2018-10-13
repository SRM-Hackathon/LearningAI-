from constants import GROUP_ADMINS
from studyobjects.base import IntentHandler

# TODO
# 1. list doubts asked by me
# 2. list doubts asked by friends (all, clarified, not calrified)
# 3. give solution to doubt (once solution is given respond to the respected person)
# 4. see solution solved by friends
# 5. create doubt - only for that environment
# 6. assign doubt when doubt created will be assigned to anyone
from studyobjects.models import UserEnvironment, Doubts, DoubtsClarified
from user.models import TeamMembership
from utils import add_entity_in_dialogflow
from bot_messages.responses import DoubtResponses
from django.contrib.auth.models import Group


def notify_to_clarify_doubt(doubt_clarified):
    # TODO (Panneer) - create text format for slack
    pass


class DoubtsHandler(IntentHandler):
    def __init__(self, intent_response_dict, user, action):
        self.get_environment(user)
        super().__init__(intent_response_dict, user, action)

    def get_environment(self, user):
        self.user_environment = UserEnvironment.objects.get(user=user)

    def create(self):
        # user, description, tag, assessment
        description = self.response.get('description')
        doubt = Doubts.objects.create(
            user=self.user,
            description=description,
            tag=self.user_environment.tag,
            assessment=self.user_environment.assessment
        )
        doubt.title = doubt.tag.name + "-" +  str(doubt.id)
        doubt.save()
        self.assign_to_friends(doubt)
        add_entity_in_dialogflow("Doubt", doubt.title, [doubt.title])
        return "Doubt has been shared with friends successfully"

    def assign_to_friends(self, doubt):
        user_environment = UserEnvironment.objects.get(user=self.user)
        admin_group = Group.objects.create(name=GROUP_ADMINS)
        team_membership = TeamMembership.objects.filter(team=self.user.team).exclude(platform_user=self.user, groups=admin_group).values_list('id',flat=True)
        user = UserEnvironment.objects.filter(users__in=team_membership, assessment=user_environment.assessment).order_by('-utc_update').first()

        doubt_clarified = DoubtsClarified.objects.create(
            cleared_by=user,
            doubt=doubt
        )
        notify_to_clarify_doubt(doubt_clarified)


    def list_all(self):
        doubts = Doubts.objects.filter(
            user=self.user
        )
        if doubts:
            return
        return "No doubts asked so far"

    def list_all_solved(self):
        doubts = Doubts.objects.filter(
            user=self.user,
            is_clarified=True
        )
        if doubts:
            return
        return "No doubts asked so far"

    def list_all_un_solved(self):
        doubts = Doubts.objects.filter(
            user=self.user,
            is_clarified=False
        )
        if doubts:
            return
        return "No doubts asked so far"

    def list_doubts_assigned_to_me(self):
        doubts = DoubtsClarified.objects.filter(
            user=self.user
        )
        if doubts:
            return
        return "No doubts asked so far"

    def list_solved_doubts_assigned_to_me(self):
        doubts = DoubtsClarified.objects.filter(
            user=self.user,
            is_clarified=True
        )
        if doubts:
            return
        return "No doubts asked so far"

    def list_un_solved_doubts_assigned_to_me(self):
        doubts = DoubtsClarified.objects.filter(
            user=self.user,
            is_clarified=False
        )
        response = DoubtResponses.list_unsolved_doubts_assigned_to_me_msg(doubts)
        return response



