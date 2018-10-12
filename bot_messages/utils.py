import apiai
import json

from django.conf import settings


def detect_intent_with_text_inputs(query_text, session_id):
    ai = apiai.ApiAI(settings.CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.session_id = session_id
    request.query = query_text
    response = request.getresponse()
    return json.loads(response.read())


def days_hours_minutes(td):
   return td.days, td.seconds//3600, (td.seconds//60)%60


def format_date_hours_minutes_worked(days, hours, minutes):
   response_string =""
   is_component_present = False
   if days != 0:
       if days > 1:
           response_string = response_string + "{0} days".format(days)
       else:
           response_string = response_string + "{0} day".format(days)
       is_component_present = True

   if hours != 0:
       if is_component_present:
           response_string = response_string + ", "
       if hours > 1:
           response_string = response_string + "{0} hours".format(hours)
       else:
           response_string = response_string + "{0} hour".format(hours)
       is_component_present = True

   if minutes != 0:
       if is_component_present:
           response_string = response_string + " " + "and "

       if minutes > 1:
           response_string = response_string + "{0} minutes".format(minutes)
       else:
           response_string = response_string + "{0} minute".format(minutes)
   return response_string


def format_end_session_response(days, hours, minutes, task_name):
    if hours == 0 and minutes == 0:
        response = "You haven't learnt for a minute."

    else:
        work_time_string = format_date_hours_minutes_worked(days, hours, minutes)
        response = "Ending learning session, you've learnt on `{0}` for {1}.".format(task_name, work_time_string)
    return response


def get_task_detail_display_attachment(title, task_name, tag_name, deadline, student, eta, completion_value, time_spent):
    STANDARD_COLOR_CODE = "#164bdd"
    payload =  {
        "color": STANDARD_COLOR_CODE,
        "title": title,
        "fields": [
            {
                "title": "Task name",
                "value": task_name,
                "short": "false"
            },
            {
                "title": "Tag",
                "value": tag_name,
                "short": "false"
            },
            {
                "title": "Student",
                "value": student,
                "short": "false"
            },
            {
                "title": "Deadline",
                "value": deadline,
                "short": "false"
            },
            {
                "title": "Total time spent",
                "value": time_spent,
                "short": "false"
            },
            {
                "title": "Progress",
                "value": str(completion_value) + "%",
                "short": "false"
            },
            {
                "title": "eta",
                "value": str(eta),
                "short": "false"
            }

        ],
        "footer": "Zoey Analytics"
    }
    return payload