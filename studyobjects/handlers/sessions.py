from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from studyobjects.base import IntentHandler
from studyobjects.models import Task, UserEnvironment, UserSession
import datetime
from bot_messages.responses import SessionResponses
from django.db.models import Q


def get_total_time_spent(user_sessions):
    duration_spent = datetime.timedelta()
    for session_time in user_sessions:
        end_time = session_time["end_time"] or timezone.now()
        duration_spent = duration_spent + (end_time - session_time['start_time'])
    return duration_spent


def time_spent_on_task(task_name, user):
    user_environment = UserEnvironment.objects.get(user=user)
    task = Task.objects.get(
        name=task_name,
        student=user,
        assessment=user_environment.assessment
    )
    # TODO(Sricharan) Replace Current session endtime with current time.
    user_sessions = UserSession.objects.filter(user=user, task=task).\
        exclude(termination_type=None, start_time=None).\
        values('start_time', 'end_time')
    print(user_sessions.values())
    total_duration_spent = get_total_time_spent(user_sessions)
    return task, total_duration_spent


class SessionHandler(IntentHandler):
    """
     TODO
     1. No task is there, ask him to create tasks
     2. environment is set in default (assessment and tasks are needed)
    """

    def __init__(self, intent_response_dict, user, action):
        self.get_environment(user)
        super().__init__(intent_response_dict, user, action)

    def get_environment(self, user):
        self.user_environment = UserEnvironment.objects.get(user=user)

    def get_task(self):
        print(self.response)
        slugified_task_name = self.response.get('Task')

        self.task = Task.objects.get(
            name=slugified_task_name,
            student=self.user,
            assessment=self.user_environment.assessment
        )
        return self.task

    def get_object(self):
        try:
            self.session = UserSession.objects.get(user=self.user, end_time=None)
            return self.session
        except ObjectDoesNotExist:
            return None


    def create(self, is_master=True):
        task = self.get_task()
        response = SessionResponses.create_msg(task)
        if task:
            self.create_task_internal(task)
            return response.get("SUCCESS")
        return response.get("FAILURE")


    def breaksession(self):
        user_session = self.get_object()
        if not user_session:
            return SessionResponses.no_active_session_exists()
        task = user_session.task
        response = SessionResponses.break_session_msg(task)
        if user_session:
            user_session.end_time = timezone.now()
            user_session.termination_type = UserSession.BREAK_TERMINATION
            user_session.save()
            return response.get("SUCCESS")
        return response.get("FAILURE")

    def end(self):
        user_session = self.get_object()
        if not user_session:
            return SessionResponses.no_active_session_exists()
        if user_session:
            user_session.end_time = timezone.now()
            user_session.termination_type = UserSession.NORMAL_TERMINATION
            user_session.save()
            task = user_session.task
            user = self.user
            current_master_session = UserSession.objects.filter(
                user=user, task=task, is_master=True
            ).last()
            user_sessions = UserSession.objects.filter(
                user=user, task=task,  start_time__gte=current_master_session.start_time
            ).values('start_time', 'end_time')
            time_spent_in_current_session = get_total_time_spent(user_sessions)
            response = SessionResponses.end_session_msg(task.name, time_spent_in_current_session)
            return response

    def get_time_spent_on_current_session(self):
        self.current_session = self.get_object()
        if not self.current_session:
            return SessionResponses.no_active_session_exists()
        time_spent = timezone.now() - self.current_session.start_time
        return SessionResponses.time_spent_msg(self.current_session.task.name, time_spent)


    def resume(self):
        # if previous session is break create new session
        # if previous session is not break create a new master session
        if self.get_object():
            return None
        last_session = UserSession.objects.filter(user=self.user).last()
        task = last_session.task
        if last_session.termination_type is None or last_session.termination_type == UserSession.NORMAL_TERMINATION:
            self.create_task_internal(task)
        elif last_session.termination_type == UserSession.BREAK_TERMINATION:
            self.create_task_internal(task, is_master=False)
        print(task.__dict__)
        print(task.name)
        response = SessionResponses.resume_session_msg(task)
        return response.get("SUCCESS")

    def create_task_internal(self, task, is_master=True):
        # TODO(Panneer) please change
        last_session = UserSession.objects.filter(user=self.user).last()
        if last_session:
            if not last_session.end_time:
                last_session.end_time = timezone.now()
            last_session.save()
        response = SessionResponses.create_msg(task)
        if task:
            self.session = UserSession.objects.create(
                user=self.user,
                task=task,
                is_master=is_master
            )
            task.state = Task.IN_PROGRESS
            task.save()
            return response.get("SUCCESS")
        return response.get("FAILURE")

    def time_stats(self):
        print(self.response)
        task_name = self.response["task"]
        user = self.user
        task, duration_spent = time_spent_on_task(task_name, user)
        response = SessionResponses.time_stats_response("Time stats", task, duration_spent)
        return response