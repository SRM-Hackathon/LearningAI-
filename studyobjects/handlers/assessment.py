from django.utils import timezone

from studyobjects.base import IntentHandler
from studyobjects.models import Assessment, Course, Tag
from user.models import TeamMembership


class AssessmentHandler(IntentHandler):

    def create(self):
        course_name = self.response.get("course")
        list_tags = self.response.get("tags")
        datetime = self.response.get("datetime")
        course = Course.objects.get(team=self.user.team, name=course_name)
        name = course_name + '_' + str(datetime)
        assessment = Assessment.objects.create(
            course=course,
            name=name,
            scheduled_at=datetime,
            created_by=self.user
        )
        for tag in list_tags:
            tag = Tag.objects.get(name=tag, course=course)
            print(tag)
            assessment.tags.add(tag)
        assessment.save()
        return True

    def list_assessments(self):
        course = self.response.get("course")
        course_object = Course.objects.get(team=self.user.team, instructor=self.user, name=course)
        try:
            assessments = Assessment.objects.get(course=course_object)
            return assessments
        except Exception:
            return None

