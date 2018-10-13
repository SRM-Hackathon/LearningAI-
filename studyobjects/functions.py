import json

from bot_messages.utils import create_interactive_message
from utils import create_context


def create_context_for_eta_updation(task_name, user_id):
    context_dict = {"name": "set_eta", "lifespan": 5, "parameters": {"task": task_name}}
    request_dict = json.dumps(context_dict)
    status = create_context(user_id, request_dict)
    print(status)
    return status


def create_select_tag_payload(tags):
    payload = {
        "text": "Hey, choose the tag(concept) that you are going to focus now.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "user_id",
        "actions": []
    }
    action = {
        "name": "Tags",
        "text": "Choose a tag",
        "type": "select",
        "options": []
    }
    options = action["options"]
    for tag in tags:
        text = tag.name
        value = tag.id
        options.append(
            {
                "text": text,
                "value": value
            }
        )
    action["options"] = options
    payload["actions"].append(action)
    print(payload)
    return create_interactive_message("", payload)
