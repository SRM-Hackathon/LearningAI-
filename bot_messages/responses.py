from bot_messages.utils import get_task_detail_display_attachment
from bot_messages.utils import days_hours_minutes, format_date_hours_minutes_worked

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
    def total_time_spent_on_task(cls, task, duration_spent):
        title = "Task stats"
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



