from studyobjects.base import IntentHandler
from studyobjects.models import Course
from studyobjects.permissions.course import CourseHandlerCustomPermissions
from user.models import TeamMembership


class CourseHandler(IntentHandler):

    class Meta:
        permission_class = CourseHandlerCustomPermissions

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
        return True
