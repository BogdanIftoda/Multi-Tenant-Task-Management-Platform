from functools import wraps


def filter_by_role_and_organization(get_queryset_func):
    """
    A decorator that filters a queryset based on the user's role and organization.
    If the user is a superuser, they get access to all records.
    If the user is an admin/user, they can access a specific organization.
    """

    @wraps(get_queryset_func)
    def wrapper(self, *args, **kwargs):
        user = self.request.user
        queryset = get_queryset_func(self, *args, **kwargs)
        # If the user is a superuser, return all results
        if user.role.name == user.role.SUPERUSER:
            return queryset
        else:
            return queryset.filter(organization_id=user.organization_id)

    return wrapper
