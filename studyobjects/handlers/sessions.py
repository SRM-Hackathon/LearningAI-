from django.core.exceptions import ObjectDoesNotExist

from studyobjects.base import IntentHandler
from studyobjects.models import Task, UserEnvironment, UserSession
import datetime


class SessionHandler(IntentHandler):
    """
     TODO
     1. No task is there, ask him to create tasks
     2. environment is set in default (assessment and tasks are needed)
    """

    def __init__(self, intent_response_dict, user, action):
        super().__init__(intent_response_dict, user, action)
        self.get_environment()

    def get_environment(self):
        self.user_environment = UserEnvironment.objects.get(user=self.user)

    def get_task(self):
        slugified_task_name = self.response.get('name')

        self.task = Task.objects.get(
            task_name=slugified_task_name,
            user=self.user,
            assessment=self.user_environment.assessment
        )
        return self.task

    def get_object(self):
        try:
            self.session = UserSession.objects.get(user=self.user, task=self.task).last()
            return self.session
        except ObjectDoesNotExist:
            return None

    def create(self, is_master=True):
        task = self.get_task()
        if task:
            self.session = UserSession.objects.create(
                user=self.user,
                task=task,
                is_master=is_master
            )
            return True

    def breaksession(self):
        user_session = self.get_object()
        if user_session:
            user_session.end_time = datetime.datetime.now()
            user_session.termination_type = UserSession.BREAK_TERMINATION
            user_session.save()
            return True

    def end(self):
        user_session = self.get_object()
        if user_session:
            user_session.end_time = datetime.datetime.now()
            user_session.termination_type = UserSession.NORMAL_TERMINATION
            user_session.save()
            return True

    def resume(self):
        # if previous session is break create new session
        # if previous session is not break create a new master session
        user_session = self.get_object()
        if user_session.termination_type is None or user_session.termination_type == UserSession.NORMAL_TERMINATION:
            self.create()
        elif self.session.termination_type == UserSession.BREAK_TERMINATION:
            self.create(is_master=False)


def time_spent_on_task(task_name, user):
    duration_spent = 0
    user_environment = UserEnvironment.objects.get(user=user)
    task = Task.objects.get(
        task_name=task_name,
        user=user,
        assessment=user_environment.assessment
    )
    user_session = UserSession.objects.filter(user=user, task=task).\
        exclude(termination_type=None, start_time=None, end_time=None).\
        values('start_time', 'end_time')
    for session_time in user_session:
        duration_spent = duration_spent + (session_time['end_time']-session_time['start_time'])

    return duration_spent
