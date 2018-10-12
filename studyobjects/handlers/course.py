import types

from studyobjects.base import IntentHandler
from studyobjects.models import Course, Tag, UserEnvironment
from studyobjects.permissions.course import CourseHandlerCustomPermissions
from user.models import TeamMembership
from utils import associate_course_with_users


class CourseHandler(IntentHandler):

    class Meta:
        permission_class = CourseHandlerCustomPermissions

    def create(self):
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
        alg, created = Tag.objects.get_or_create(name="algebra", course=course)
        Tag.objects.get_or_create(name="geometry", course=course)
        Tag.objects.get_or_create(name="trignometry", course=course)
        Tag.objects.get_or_create(name="arithmetic", course=course)
        associate_course_with_users(tag=alg)
        return True
