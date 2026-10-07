from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Map each role to the things it is allowed to do.
# Keys must match the Role values in accounts/models.py exactly.
ROLE_PERMISSIONS = {
    'ADMIN': {
        'manage_staff', 'register_patient', 'search_patient',
        'book_appointment', 'view_medical_records',
    },
    'RECEPTIONIST': {
        'register_patient', 'search_patient', 'book_appointment',
    },
    'PHYSICIAN': {
        'search_patient', 'view_medical_records', 'view_appointments',
    },
    'NURSE': {
        'search_patient', 'view_medical_records', 'view_appointments',
    },
    # add the other SO-8 roles here as needed
}


def get_user_role(user):
    """Return the role of a logged-in user, or None."""
    if not user.is_authenticated:
        return None
    return getattr(user, 'role', None)


def get_permissions(user):
    """Return the set of permissions for this user."""
    if not user.is_authenticated:
        return set()
    if user.is_superuser:
        return set().union(*ROLE_PERMISSIONS.values())
    return ROLE_PERMISSIONS.get(get_user_role(user), set())


def has_permission(user, permission):
    return permission in get_permissions(user)


def permission_required_for(permission):
    """Decorator: user must be logged in AND have this permission."""
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not has_permission(request.user, permission):
                raise PermissionDenied   # shows a 403 page
            return view(request, *args, **kwargs)
        return login_required(wrapper)   # not logged in -> redirected to login
    return decorator