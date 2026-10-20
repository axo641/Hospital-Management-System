from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .permissions import get_permissions, get_user_role

@login_required
def dashboard(request):
    """Dashboard view - shows options based on user's role and permissions"""
    user = request.user
    user_role = get_user_role(user)
    role_perms = get_permissions(user)
    
    context = {
        'user_role': user_role if user_role else 'No Role Assigned',
        'role_perms': role_perms,
    }
    
    return render(request, 'accounts/dashboard.html', context)
