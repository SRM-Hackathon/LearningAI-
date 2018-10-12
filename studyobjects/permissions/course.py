from constants import GROUP_ADMINS
from studyobjects.base import PermissionsRunner
from studyobjects.permissions.functions import is_user_in_subset_of_groups


class CourseHandlerCustomPermissions(PermissionsRunner):

    def has_permission(self):
        return is_user_in_subset_of_groups(self.user, [GROUP_ADMINS])
