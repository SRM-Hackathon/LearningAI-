import json
import requests


from celery.decorators import task

from studyobjects.functions import create_context_for_eta_updation
from studyobjects.models import Task
from user.models import PlatformUser

NODE_BASE_ENDPOINT = "http://localhost:3000"


@task(name="ask_for_update_when_eta_expires")
def ask_for_update_when_eta_expires(*args):
    user = args[0]
    task_id = args[1]
    team_id = args[2]
    task = Task.objects.get(id=task_id)
    create_context_for_eta_updation(task.name, user)
    channel_id = PlatformUser.objects.get(identity=user).channel_id
    data = {
        "channels": [channel_id, ],
        "message": "Hey, looks like you've studied for longtime. Can you tell me how much time it will take?",
        "team": team_id
    }
    print(data)
    url = NODE_BASE_ENDPOINT + "/notify/channels"
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)


@task(name="notify_person_who_asked_doubt")
def notify_person_who_asked_doubt(*args):
    user = args[0]
    response = args[1]
    team_id = args[2]
    channel_id = PlatformUser.objects.get(identity=user).channel_id
    data = {
        "channels": [channel_id, ],
        "message": response,
        "team": team_id
    }
    print(data)
    url = NODE_BASE_ENDPOINT + "/notify/channels"
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)
