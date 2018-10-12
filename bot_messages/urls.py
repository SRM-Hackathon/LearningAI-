from django.urls import path

from bot_messages.views import send_to_dialogflow

urlpatterns = [
    path('send', send_to_dialogflow),
]
