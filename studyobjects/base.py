import types


class IntentHandler:

    def __init__(self, intent_response_dict, user, action):
        self.response = intent_response_dict
        self.user = user
        self.action = action
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, types.FunctionType):
                if action == value.__name__:
                    value(self)


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
