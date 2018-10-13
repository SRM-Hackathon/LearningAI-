from bot_messages.utils import get_task_detail_display_attachment
from bot_messages.utils import days_hours_minutes, format_date_hours_minutes_worked, format_end_session_response
from bot_messages.utils import build_doubt_attachment_payload

class TaskResponses:

    @classmethod
    def upgrade_status_msg(cls, task_name=None, dest_state=None, failure_msg=None):

        if failure_msg:
            return failure_msg

        return "The state of your task, {task_name} is moved to {dest}".format(
            task_name=task_name,  dest=dest_state.lower(),
        )

class SessionResponses:

    @classmethod
    def time_stats_response(cls, title, task, duration_spent):
        task_name = task.tag.name
        tag_name = task.tag.name
        deadline = task.assessment.scheduled_at
        student = task.student.platform_user
        eta = task.eta
        completion_value = task.progress
        duration_spent_response = format_date_hours_minutes_worked(
            days_hours_minutes(duration_spent)
        )
        return get_task_detail_display_attachment(
            title, task_name, tag_name, deadline, student, eta, completion_value, duration_spent_response
        )

    @classmethod
    def end_session_msg(cls, task_name, duration_spent):
        days, hours, minutes = days_hours_minutes(duration_spent)
        return format_end_session_response(days, hours, minutes, task_name)

    @classmethod
    def create_msg(cls, task):
        return {
            "SUCCESS": "Cool.. Your session on {} starts now".format(task),
            "FAILURE": "Couldn't start your session. Check if a task by the name {} exists".format(task.name)
        }

    @classmethod
    def break_session_msg(cls, task):
        return {
            "SUCCESS": "Okay.. Your session on {} is paused. Continue after your break".format(task.name),
            "FAILURE": "Couldn't pause your session. Check if a task by the name {} exists".format(task.name)
        }

    @classmethod
    def resume_session_msg(cls, task):
        return {
            "SUCCESS": "Awesome.. Your are resuming your session on {}".format(task.name),
            "FAILURE": "Couldn't find your session. Check if a task by the name {} exists".format(task.name)
        }


class DoubtResponses:

    @classmethod
    def list_unsolved_doubts_assigned_to_me_msg(cls, doubts):
        if len(doubts) == 0:
            return "You don't have any doubts to answer"

        return build_doubt_attachment_payload(doubts, "Doubts")