from datetime import timedelta
from slugify import slugify

from django.utils import timezone

from bot_messages.utils import get_task_detail_display_attachment, create_interactive_message
from studyobjects.base import IntentHandler
from studyobjects.models import Course, UserEnvironment, Task
from studyobjects.tasks import ask_for_update_when_eta_expires
from user.models import TeamMembership
from utils import get_displaced_time_from_duration_entity, add_entity_in_dialogflow, format_date_and_time
from bot_messages.responses import TaskResponses, SessionResponses
from bot_messages.responses import FAILURE, SUCCESS


class TaskHandler(IntentHandler):

    def set_eta(self, task, dt):
        identity = task.student.platform_user.identity
        task.eta = dt
        task.save()
        # ask_for_update_when_eta_expires.apply_async(
        #     args=[task.student.platform_user.identity],
        #     eta=dt
        # )
        ask_for_update_when_eta_expires(identity)

    def __init__(self, intent_response_dict, user, action):
        self.user_environment = UserEnvironment.objects.get(user=user)
        super().__init__(intent_response_dict, user, action)

    def create(self):
        ask_for_update_when_eta_expires(self.user.platform_user.identity)
        return False
        name = self.response["name"]
        formatted_task_name = slugify(self.response["name"])
        eta = get_displaced_time_from_duration_entity(timezone.now(), self.response["eta"])
        assessment = self.user_environment.assessment
        tag = self.user_environment.tag
        task, created = Task.objects.get_or_create(
            name=formatted_task_name,
            assessment=assessment,
            tag=tag,
            student=self.user,
        )
        self.set_eta(task, eta)
        add_entity_in_dialogflow("Task", formatted_task_name, [name, ])
        return SessionResponses.time_stats_response("New task added!", task, timedelta())


    def get_task_object(self):
        name = self.response["name"]
        if not name:
            return None
        try:
            task = Task.objets.get(
                student=self.user,
                name=name,
                assessment=self.user_environment.assessment,
                tag=self.user_environment.tag
            )
            return task
        except Task.DoesNotExist:
            return "Task is not available"

    def upgrade_state(self):
        task_name = self.response["task"]
        team_membership_user = self.user
        user_environment = UserEnvironment.objects.get(user=self.user)
        assessment = user_environment.assessment
        task = Task.objects.get(assessment=assessment, name=task_name, student=team_membership_user)
        dest_status = task.upgrade_state()
        if dest_status is None:
            return TaskResponses.upgrade_status_msg(
                failure_msg="State of a completed task cannot upgraded."
            )
        else:
            return TaskResponses.upgrade_status_msg(
                task.name, dest_status
            )

    def listall(self):
        # added in intent dialog flow
        tasks = Task.objects.filter(
            student=self.user,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = format_tasks(tasks)
        print(formatted_task_names)
        return formatted_task_names

    def listtodo(self):
        # added in intent dialog flow
        tasks = Task.objects.filter(
            student=self.user,
            state=Task.TODO,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = format_tasks(tasks)
        return formatted_task_names

    def listinprogress(self):
        # added in intent dialog flow
        tasks = Task.objects.filter(
            student=self.user,
            state=Task.IN_PROGRESS,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = format_tasks(tasks)
        if tasks:
            return SessionResponses.list_tasks_msg(formatted_task_names).get(SUCCESS)
        return SessionResponses.list_tasks_msg("In Progress").get(FAILURE)

    def listcompleted(self):
        # added in intent dialog flow
        tasks = Task.objects.filter(
            student=self.user,
            state=Task.COMPLETED,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = format_tasks(tasks)
        return formatted_task_names


    def update_progress_in_task(self):
        task_name = self.response["task"]
        completion_value_in_percent = self.response["completion_value"]
        completion_value_percent_symbol_index = completion_value_in_percent.find("%")
        completion_value = int(completion_value_in_percent[:completion_value_percent_symbol_index])
        assessment = UserEnvironment.objects.get(user=self.user).assessment
        task = Task.objects.get(
            name=task_name,
            student=self.user,
            assessment=assessment
        )
        task.progress = completion_value
        task.save()
        return True


def format_tasks(tasks):
    return "{}".format("\n".join(tasks))
