from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment
from .models import Patient
from accounts.permissions import permission_required_for


@login_required
@permission_required_for('book_appointment')
def appointment_list(request):
    """Display list of appointments based on user role
    - Doctors/Physicians see only their appointments
    - Admins/Clerks see all appointments
    """
    user = request.user
    
    # If user is a doctor/physician, show only their appointments
    if user.role in ['PHYSICIAN', 'SURGEON', 'RADIOLOGIST']:
        appointments = Appointment.objects.filter(doctor=user).order_by('date', 'time')
    else:
        # Admin, executives, clerks see all appointments
        appointments = Appointment.objects.all().order_by('date', 'time')
    
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})


@login_required
@permission_required_for('book_appointment')
def create_appointment(request):
    """Create a new appointment - tracked user info"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/create_appointment.html', {'form': form})


@login_required
@permission_required_for('book_appointment')
def edit_appointment(request, appointment_id):
    """Edit an existing appointment - only if user is doctor or admin"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    user = request.user
    
    # Only allow doctor or admin to edit
    if user.role not in ['ADMIN', 'EXECUTIVE', 'CLERK'] and appointment.doctor != user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/edit_appointment.html', {'form': form, 'appointment': appointment})


@login_required
@permission_required_for('book_appointment')
def delete_appointment(request, appointment_id):
    """Delete an appointment - only if user is doctor or admin"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    user = request.user
    
    # Only allow doctor or admin to delete
    if user.role not in ['ADMIN', 'EXECUTIVE', 'CLERK'] and appointment.doctor != user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    
    return render(request, 'appointments/delete_appointment.html', {'appointment': appointment})
