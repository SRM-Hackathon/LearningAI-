from constants import GROUP_COURSE_INSTRUCTORS
from decorators import access_gateway
from studyobjects.models import Assessment


access_gateway([GROUP_COURSE_INSTRUCTORS, ])
def create_assessment(parameter_dict, team_membership):
    course = parameter_dict['course'].string_value
    name = parameter_dict['name'].string_value
    list_tags = parameter_dict['tags'].list_value.values
    tags = []
    for item in list_tags:
        tags.append(item.string_value)
    datetime = parameter_dict['datetime'].struct_value.fields['date_time'].string_value
    Assessment.objects.create(
        course=course,
        name=name,
        tags=tags,
        scheduled_at=datetime,
        created_by=team_membership
    )
    return True
