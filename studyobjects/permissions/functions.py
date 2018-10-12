
def is_user_in_subset_of_groups(team_membership, groups):
    if team_membership.groups.filter(name__in=groups).exists():
        return True
    return False
