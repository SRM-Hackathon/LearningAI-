import json
import requests


from celery.decorators import task
from celery.decorators import periodic_task
from celery.schedules import crontab
from django.db.models import Count, Sum, F
from django.utils import timezone

from bot_messages.utils import create_student_poor_performance_payload, create_interactive_message
from studyobjects.functions import create_context_for_eta_updation
from studyobjects.models import Task
from user.models import PlatformUser, Team, TeamMembership

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


@periodic_task(run_every=crontab(minute='*/1'))
def notify_teacher_when_score_dips():
    teams = Team.objects.all()
    for team in teams:
        tm = TeamMembership.objects.filter(team=team).order_by('utc_created').first()
        user = tm.platform_user.identity
        team_id = team.identity
        channel_id = PlatformUser.objects.get(identity=user).channel_id
        payload = create_student_poor_performance_payload(user)
        data = {
            "channels": [channel_id, ],
            "attachments": create_interactive_message("Attention required", payload),
            "team": team_id
        }
        print(data)
        url = NODE_BASE_ENDPOINT + "/notify/channels"
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=json.dumps(data), headers=headers)
