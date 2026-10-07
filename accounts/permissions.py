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
    'PHYSICIAN': {
        'search_patient', 'view_medical_records', 'book_appointment',
    },
    'SURGEON': {
        'search_patient', 'view_medical_records', 'book_appointment',
    },
    'NURSE': {
        'search_patient', 'view_medical_records', 'book_appointment',
    },
    'PHARMACIST': {
        'search_patient', 'view_medical_records',
    },
    'PHYSIOTHERAPIST': {
        'search_patient', 'view_medical_records', 'book_appointment',
    },
    'RADIOLOGIST': {
        'search_patient', 'view_medical_records', 'book_appointment',
    },
    'TECHNICIAN': {
        'search_patient', 'view_medical_records',
    },
    'EXECUTIVE': {
        'manage_staff', 'search_patient', 'view_medical_records',
    },
    'CLERK': {
        'register_patient', 'search_patient', 'book_appointment',
    },
    'OFFICE_ASSISTANT': {
        'register_patient', 'search_patient', 'book_appointment',
    },
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
    user_role = get_user_role(user)
    return ROLE_PERMISSIONS.get(user_role, set())


def has_permission(user, permission):
    """Check if user has a specific permission."""
    return permission in get_permissions(user)


def permission_required_for(permission):
    """Decorator: user must be logged in AND have this permission."""
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # User not logged in, redirect to login
                return login_required(lambda r: None)(request)
            if not has_permission(request.user, permission):
                # User logged in but doesn't have permission
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
