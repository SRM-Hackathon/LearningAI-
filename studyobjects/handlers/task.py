from datetime import timedelta
from slugify import slugify

from django.utils import timezone

from studyobjects.base import IntentHandler
from studyobjects.models import Course, UserEnvironment, Task
from user.models import TeamMembership
from utils import get_displaced_time_from_duration_entity, add_entity_in_dialogflow


class TaskHandler(IntentHandler):
    def __init__(self, intent_response_dict, user, action):
        super().__init__(intent_response_dict, user, action)
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

    def list_todo(self):
        tasks = Task.objets.filter(
            student=self.user,
            state=Task.TODO,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = "{}".format("\n".join(tasks))
        return formatted_task_names

    def list_inprogress(self):
        tasks = Task.objets.filter(
            student=self.user,
            state=Task.IN_PROGRESS,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = "{}".format("\n".join(tasks))
        return formatted_task_names

    def list_completed(self):
        tasks = Task.objets.filter(
            student=self.user,
            state=Task.COMPLETED,
            assessment=self.user_environment.assessment,
            tag=self.user_environment.tag
        ).values_list('name', flat=True)
        formatted_task_names = "{}".format("\n".join(tasks))
        return formatted_task_names
