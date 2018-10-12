from datetime import timedelta
from slugify import slugify

from django.utils import timezone

from studyobjects.base import IntentHandler
from studyobjects.models import Course
from user.models import TeamMembership


class TaskHandler(IntentHandler):


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
        task_name = self.response.get("name")
        formatted_task_name = slugify(task_name)
        eta = self.response.get("eta")
        duration_magnitude = eta["amount"]
        unit = eta["unit"]
        # TODO(Sricharan) Make a utility for duration values.
        if unit == 'h':
            eta = timezone.now() + timedelta(hours=duration_magnitude)
        elif unit == 'm':
            eta = timezone.now() + timedelta(minutes=duration_magnitude)
        print(eta)
        print(formatted_task_name)
        return
        team = self.user.team
        instructor_membership = TeamMembership.objects.get(team=team, platform_user__identity=course_instructor_id)
        Course.objects.get_or_create(
            name=course_name,
            team=team,
            defaults={'instructor': instructor_membership}
        )
        group, created = Group.objects.get_or_create(name=GROUP_COURSE_INSTRUCTORS)
        group.team_memberships.add(instructor_membership)
        group.save()
        return True