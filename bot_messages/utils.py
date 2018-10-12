import apiai
import json

from django.conf import settings


def detect_intent_with_text_inputs(query_text, session_id):

    ai = apiai.ApiAI(settings.CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.session_id = session_id
    request.query = query_text
    response = request.getresponse()
    return json.loads(response.read())
