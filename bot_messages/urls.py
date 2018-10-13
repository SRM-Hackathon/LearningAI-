from django.urls import path

from bot_messages.views import send_to_dialogflow, handle_slack_interaction

urlpatterns = [
    path('send', send_to_dialogflow),
    path('slack/interaction', handle_slack_interaction),
]
