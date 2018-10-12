from django.contrib.auth.models import Group

from constants import GROUP_COURSE_INSTRUCTORS
from studyobjects.base import IntentHandler
from studyobjects.models import Course
from studyobjects.permissions.course import CourseHandlerCustomPermissions
from user.models import TeamMembership


class CourseHandler(IntentHandler):

    class Meta:
        permission_class = CourseHandlerCustomPermissions

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
        course_name = self.response.get("course")
        course_instructor_id = self.response.get("instructor")
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
