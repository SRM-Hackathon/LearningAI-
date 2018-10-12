import types

from studyobjects.base import IntentHandler
from studyobjects.models import Course, Tag
from studyobjects.permissions.course import CourseHandlerCustomPermissions
from user.models import TeamMembership


class CourseHandler(IntentHandler):

    class Meta:
        permission_class = CourseHandlerCustomPermissions

    def create(self):
        print(self.response)
        course_name = self.response.get("name")
        course_instructor_id = self.response.get("instructor")
        team = self.user.team
        instructor_membership = TeamMembership.objects.get(team=team, platform_user__identity=course_instructor_id)
        course, created = Course.objects.get_or_create(
            name=course_name,
            team=team,
            defaults={'instructor': instructor_membership}
        )
        #TODO(Sricharan) To be removed.
        Tag.objects.get_or_create(name="algebra", course=course)
        Tag.objects.get_or_create(name="geometry", course=course)
        Tag.objects.get_or_create(name="trignometry", course=course)
        Tag.objects.get_or_create(name="arithmetic", course=course)
        return True
