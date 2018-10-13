from studyobjects.base import IntentHandler

# TODO
# 1. list doubts asked by me
# 2. list doubts asked by friends (all, clarified, not calrified)
# 3. give solution to doubt (once solution is given respond to the respected person)
# 4. see solution solved by friends
# 5. create doubt - only for that environment
# 6. assign doubt when doubt created will be assigned to anyone
from studyobjects.models import UserEnvironment, Doubts, DoubtsClarified
from utils import add_entity_in_dialogflow


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
        self.assign_to_friends()
        add_entity_in_dialogflow("Doubt", doubt.title, [doubt.title])
        return "Doubt has been shared with friends successfully"

    def assign_to_friends(self):
        pass

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
        if doubts:
            return
        return "No doubts asked so far"




