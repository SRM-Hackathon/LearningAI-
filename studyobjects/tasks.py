import json
import requests

from celery.decorators import task

from user.models import PlatformUser

NODE_BASE_ENDPOINT = "http://0.0.0.0:3000"

url = NODE_BASE_ENDPOINT + "/notify/channels"
requests.get(url)

@task(name="ask_for_update_when_eta_expires")
def ask_for_update_when_eta_expires(user):
    channel_id = PlatformUser.objects.get(identity=user).channel_id
    data = {
        "channels": [channel_id, ],
        "message": "ETA expired"
    }
    url = NODE_BASE_ENDPOINT + "/notify/channels"
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)
