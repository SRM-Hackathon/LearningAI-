import apiai
import json

from django.conf import settings


def format_user_id(unique_id):
    return "<@{0}>".format(unique_id)


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
   if not days and not hours and not minutes:
       response_string = "-"
       return response_string

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


def format_time_spent(days, hours, minutes, task_name):
    if hours == 0 and minutes == 0:
        response = "You haven't learnt for a minute."

    else:
        work_time_string = format_date_hours_minutes_worked(days, hours, minutes)
        response = "You have been learning {0} for {1} now.".format(task_name, work_time_string)
    return response


def create_interactive_message(text, attachment):
    return {
        "attachments": [attachment],
        "text": text
    }

def create_student_poor_performance_payload(user):
    STANDARD_COLOR_CODE = "#FF0000"
    unique_id = format_user_id(user)
    analysis = """I find that he is not tracking consistently. 
    Takes up a high number of tasks, but does'nt complete them.
    Looks especially weak in Algebra."""
    payload = {
        "color": STANDARD_COLOR_CODE,
        "title": "The performance of this student is going down",
        "fields": [
            {
                "title": "Student name",
                "value": unique_id,
                "short": "false"
            },
            {
                "title": "Score",
                "value": "27",
                "short": "false"
            },
            {
                "title": "Analysis",
                "value": analysis,
                "short": "true"
            },
        ],
        "footer": "Zoey Analytics"
    }
    return payload

def get_task_detail_display_attachment(title, task_name, tag_name, deadline, student, eta, completion_value, time_spent):
    STANDARD_COLOR_CODE = "#164bdd"
    payload = {
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
                "value": format_user_id(student),
                "short": "false"
            },
            {
                "title": "Deadline",
                "value": str(deadline),
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

def build_doubt_attachment_payload(doubts, card_title):
    STANDARD_COLOR_CODE = "#164bdd"
    fields = []
    for doubt in doubts:
        field_dict = {}
        field_dict["title"] = doubt.title
        field_dict["value"] = doubt.description
        field_dict["short"] = "false"
        fields.append(field_dict)

    payload = {
        "color": STANDARD_COLOR_CODE,
        "title": card_title,
        "fields": fields,
        "footer": "Zoey Doubt assist"
    }
    return create_interactive_message("", payload)
