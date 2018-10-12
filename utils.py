import json

import apiai

from datetime import timedelta

import requests

from learning_dot_ai.settings import CLIENT_ACCESS_TOKEN, DEVELOPER_ACCESS_TOKEN, ENTITY_ADDITION_URL, DEVELOPER_HEADERS


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
