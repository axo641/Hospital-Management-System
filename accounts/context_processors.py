from .permissions import get_permissions, get_user_role

def role_info(request):
    return {
        'user_role': get_user_role(request.user),
        'role_perms': get_permissions(request.user),
    }