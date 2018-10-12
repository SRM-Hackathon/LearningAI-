class TaskResponses:

    @classmethod
    def upgrade_status_msg(cls, task_name=None, dest_state=None, failure_msg=None):

        if failure_msg:
            return failure_msg

        return "The state of your task, {task_name} is moved to {dest}".format(
            task_name=task_name,  dest=dest_state.lower(),
        )