from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, StaffCreationForm
from .models import User
from .permissions import permission_required_for

# Create your views here.

def userLogin(request):
    """Handle user login - tracks logged in user automatically via request.user"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # User is now tracked in request.user and session
                return redirect('home')
            else:
                return render(request, 'accounts/login.html',
                              {'form': form, 'error': 'Invalid username or password.'})
        else:
            return render(request, 'accounts/login.html',
                          {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
@permission_required_for('manage_staff')
def staff_list(request):
    """Display list of all staff members - Only accessible to ADMIN and EXECUTIVE"""
    staff = User.objects.all().order_by('first_name')
    return render(request, 'accounts/staff_list.html', {'staff': staff})


@login_required
@permission_required_for('manage_staff')
def create_staff(request):
    """Create a new staff member - Only accessible to ADMIN and EXECUTIVE"""
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffCreationForm()

    return render(request, 'accounts/create_staff.html', {'form': form})


@login_required
@permission_required_for('manage_staff')
def edit_staff(request, staff_id):
    """Edit an existing staff member - Only accessible to ADMIN and EXECUTIVE"""
    staff = get_object_or_404(User, id=staff_id)
    
    if request.method == 'POST':
        form = StaffCreationForm(request.POST, instance=staff)
        if form.is_valid():
            if not form.cleaned_data.get('password'):
                form.instance.set_password(staff.password)
            form.save()
            return redirect('staff_list')
    else:
        form = StaffCreationForm(instance=staff)

    return render(request, 'accounts/edit_staff.html', {'form': form, 'staff': staff})


@login_required
@permission_required_for('manage_staff')
def delete_staff(request, staff_id):
    """Delete a staff member - Only accessible to ADMIN and EXECUTIVE"""
    staff = get_object_or_404(User, id=staff_id)
    
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    
    return render(request, 'accounts/delete_staff.html', {'staff': staff})


def userLogout(request):
    """Logout user - clears session and tracked user"""
    logout(request)
    return redirect('login')
