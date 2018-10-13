import json

from utils import create_context


def create_context_for_eta_updation(task_name, user_id):
    context_dict = {"name": "set_eta", "lifespan": 5, "parameters": {"task": task_name}}
    request_dict = json.dumps(context_dict)
    status = create_context(user_id, request_dict)
    print(status)
    return status


def
{
    "text": "Choose a tag",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "user_id",
    "actions": [
        {
            "name": "Tags",
            "text": "Choose a tag",
            "type": "select",
            "options": []
        }
    ]
}

