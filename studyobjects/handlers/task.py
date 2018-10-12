from datetime import timedelta
from slugify import slugify

from django.utils import timezone

from studyobjects.base import IntentHandler
from studyobjects.models import Course, UserEnvironment, Task
from user.models import TeamMembership
from utils import get_displaced_time_from_duration_entity, add_entity_in_dialogflow
from bot_messages.responses import TaskResponses

class TaskHandler(IntentHandler):
    def __init__(self, intent_response_dict, user, action):
        super().__init__(intent_response_dict, user, action)
        import ipdb;ipdb.set_trace();
        self.user_environment = UserEnvironment.objects.get(user=self.user)

    def get_object(self):
        course_name = self.response.get("course")
        if not course_name:
            return None
        try:
            self.course = Course.objects.get(name=course_name, team=self.user.team)
            return self.course
        except Course.DoesNotExist:
            return None

    def create(self):
        name = self.response["name"]
        formatted_task_name = slugify(self.response["name"])
        eta = get_displaced_time_from_duration_entity(timezone.now(), self.response["eta"])

        assessment = self.user_environment.assessment
        tag = self.user_environment.tag
        Task.objects.get_or_create(
            name=formatted_task_name,
            assessment=assessment,
            tag=tag,
            student=self.user,
            eta=eta
        )
        add_entity_in_dialogflow("Task", formatted_task_name, [name, ])
        return True

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

    def detail(self):
        task = self.get_object()
        return dict(task.values_list())

    def list_all_tasks(self):
        tasks = Task.objects.filter(
            student=self.user,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = format_tasks(tasks)
        return formatted_task_names

    def list_todo(self):
        tasks = Task.objects.filter(
            student=self.user,
            state=Task.TODO,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = format_tasks(tasks)
        return formatted_task_names

    def list_inprogress(self):
        tasks = Task.objects.filter(
            student=self.user,
            state=Task.IN_PROGRESS,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = format_tasks(tasks)
        return formatted_task_names

    def list_completed(self):
        tasks = Task.objects.filter(
            student=self.user,
            state=Task.COMPLETED,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = format_tasks(tasks)
        return formatted_task_names


def format_tasks(tasks):
    return "{}".format("\n".join(tasks))
