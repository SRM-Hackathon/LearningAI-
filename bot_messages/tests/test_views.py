import json

from unittest.mock import MagicMock

from django.test import TestCase

from bot_messages.views import send_to_dialogflow
from user.factory import UserFactory, PlatformUserFactory, TeamMembershipFactory
from user.factory import TeamFactory

class TestView(TestCase):


    def test_send_to_dialogflow(self):
        data = {
            "team": "T1345",
            "user": "UI123",
            "text": "create a task named working out math, the eta is 2 hours"
        }
        team = TeamFactory(identity="T1345")
        user = UserFactory()
        user = PlatformUserFactory(identity="UI123", user=user)
        TeamMembershipFactory(platform_user=user, team=team)
        data = json.dumps(data)
        request = MagicMock(body=data)
        send_to_dialogflow(request)
