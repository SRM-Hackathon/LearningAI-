
class Validators:

    def __init__(self, result_dict):
        self.data = result_dict

    def is_action_incomplete(self):
        return not self.data['actionIncomplete']

    def validate(self):
        return (
            self.is_action_incomplete()
        )
