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
from studyobjects.tasks import notify_person_who_asked_doubt
from user.models import TeamMembership
from utils import add_entity_in_dialogflow
from bot_messages.responses import DoubtResponses
from django.contrib.auth.models import Group


def notify_to_clarify_doubt(doubt_clarified):
    # TODO (Panneer) - create text format for slack
    pass


def notify_doubt_asked_person(doubt, clarified_response):
    notify_person_who_asked_doubt.delay(
        doubt.user.platform_user.identity,
        clarified_response,
        doubt.user.team.identity
    )


class DoubtsHandler(IntentHandler):
    def __init__(self, intent_response_dict, user, action):
        self.get_environment(user)
        super().__init__(intent_response_dict, user, action)

    def get_environment(self, user):
        self.user_environment = UserEnvironment.objects.get(user=user)

    def create(self):
        # user, description, tag, assessment
        description = self.response['description']
        print(self.response)
        doubt = Doubts.objects.create(
            user=self.user,
            description=description,
            tag=self.user_environment.tag,
            assessment=self.user_environment.assessment
        )
        doubt.title = doubt.tag.name + "-" + str(doubt.id)
        doubt.save()
        self.assign_to_friends(doubt)
        add_entity_in_dialogflow("Doubt", doubt.title, [doubt.title])

        return "Doubt has been shared with friends successfully"

    def assign_to_friends(self, doubt):
        team_membership = TeamMembership.objects.filter(
            team=self.user.team
        ).exclude(id=self.user.id).order_by('utc_created').first()
        print(team_membership.platform_user.identity)
        doubt_clarified = DoubtsClarified.objects.create(
            cleared_by=team_membership,
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
        doubts = Doubts.objects.filter(
            clarifications__cleared_by=self.user,
            is_clarified=False
        )
        response = DoubtResponses.list_unsolved_doubts_assigned_to_me_msg(doubts)
        return response

    def answer_doubt(self):
        title = self.response.get('Doubt')
        description = self.response.get('any')

        doubt = Doubts.objects.get(title=title)
        doubts_clarified = DoubtsClarified.objects.get(doubt=doubt, cleared_by=self.user)
        doubts_clarified.is_clarified = True
        doubts_clarified.clarified_response = description
        doubts_clarified.save()

        doubt.is_clarified = True
        doubt.save()
        notify_doubt_asked_person(doubt, doubts_clarified.clarified_response)
        return True
