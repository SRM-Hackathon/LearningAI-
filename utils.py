import json
import re

import apiai

from datetime import timedelta

import requests
from django.contrib.auth.models import User

from learning_dot_ai.settings import CLIENT_ACCESS_TOKEN, DEVELOPER_ACCESS_TOKEN, ENTITY_ADDITION_URL, DEVELOPER_HEADERS
from studyobjects.models import Course, Tag, UserEnvironment, Assessment
from user.factory import UserFactory
from user.models import Team, PlatformUser, TeamMembership


def get_displaced_time_from_duration_entity(current_time, duration):
    duration_magnitude = duration["amount"]
    unit = duration["unit"]
    if unit == 'h':
        displaced_time = current_time + timedelta(hours=duration_magnitude)
    elif unit == 'm':
        displaced_time = current_time + timedelta(minutes=duration_magnitude)
    else:
        displaced_time = current_time + timedelta(days=duration_magnitude)
    return displaced_time


def add_entity_in_dialogflow(entity_type, entity_name, synonyms):
    url = ENTITY_ADDITION_URL.format(entity_type)
    request_dict = {"value": entity_name, "synonyms": synonyms}
    serialized_dict = json.dumps(request_dict)
    entity_request = requests.post(
        url,
        data=serialized_dict,
        headers=DEVELOPER_HEADERS
    )
    print(entity_request.status_code)


def prepare_data_for_user(payload):
    identity = payload["user"]
    team = payload["team"]
    channel = payload["channel"]
    team, _ = Team.objects.get_or_create(identity=team)
    user, _ = User.objects.get_or_create(username=identity)
    pu, _ = PlatformUser.objects.get_or_create(identity=identity, user=user)
    tm, created = TeamMembership.objects.get_or_create(platform_user=pu, team=team)
    assessment = Assessment.objects.all().order_by('scheduled_at').first()
    if assessment:
        associate_course_with_users(assessment=assessment)


def parse_message(message):
    match = re.search("(?<=<@)\w+(?<!>)", message)
    if match:
        print("I am here")
        message = re.sub("(<@\w+>)", match.group(0), message)
    return message


def associate_course_with_users(**kwargs):
    memberships = TeamMembership.objects.all()
    for member in memberships:
        UserEnvironment.objects.update_or_create(user=member, defaults=kwargs)

def render_default_response(response_results):
    return response_results['fulfillment']['speech']
