import types


class IntentHandler:

    def __init__(self, intent_response_dict, user, action):
        self.response = intent_response_dict
        self.user = user
        self.action = action

    def execute(self):
        actual_func = None
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, types.FunctionType):
                if self.action == value.__name__:
                    actual_func = value
                    break
        return actual_func(self)


class PermissionsRunner:

    def __init__(self, user, action, object=None):
        self.user = user
        self.action = action
        if not object:
            self.has_permission()
        else:
            self.has_object_permission(object)

    def has_permission(self):
        return True

    def has_object_permission(self, object):
        return True
