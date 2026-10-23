import openpyxl
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from .forms import AppointmentForm
from .models import Appointment
from .models import Patient
from accounts.permissions import permission_required_for, has_permission


@login_required
@permission_required_for('book_appointment')
def appointment_list(request):
    """Display list of appointments based on user role
    - Doctors/Physicians see only their appointments
    - Admins/Clerks see all appointments
    """
    user = request.user
    
    if user.role in ['PHYSICIAN', 'SURGEON', 'RADIOLOGIST']:
        appointments = Appointment.objects.filter(doctor=user).order_by('date', 'time')
    else:
        appointments = Appointment.objects.all().order_by('date', 'time')
    
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments, 
        'can_view_doctor_schedule': has_permission(request.user, 'view_doctor_schedule')
    })


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
    
    if user.role not in ['ADMIN', 'EXECUTIVE', 'CLERK'] and appointment.doctor != user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    
    return render(request, 'appointments/delete_appointment.html', {'appointment': appointment})


@login_required
@permission_required_for('view_doctor_schedule')
def doctor_schedule(request):
    today = timezone.localdate()
    doctor = request.user
    view_type = request.GET.get('view', 'today')

    if view_type not in ['today', 'week']:
        view_type = 'today'

    appointments = Appointment.objects.filter(doctor=doctor)
    
    if view_type == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        appointments = appointments.filter(date__range=[start_date, end_date])
    else:
        appointments = appointments.filter(date=today)

    appointments = appointments.order_by('date', 'time')
    return render(request, 'appointments/doctor_schedule.html', {
        'appointments': appointments, 'view_type': view_type, 'today': today,
    })


def check_patient_in(request, appointmentID):
    appointment = get_object_or_404(Appointment, id=appointmentID)

    if request.method == 'POST':
        appointment.is_checked_in = True
        appointment.arrival_time = timezone.now()
        appointment.save()

        return redirect('appointment_list')

    context = {
        'appointment': appointment,
        'appointmentID': appointmentID,
    }

    return render(request, 'appointments/check_in.html', context)


@login_required
@permission_required_for('view_own_appointments')
def patient_appointments_dashboard(request):
    """Fetch appointments only for the Patient instance connected to the logged-in User profile names."""
    try:
        patient_profile = Patient.objects.get(
            first_name__iexact=request.user.first_name, 
            last_name__iexact=request.user.last_name
        )
        appointments = Appointment.objects.filter(patient=patient_profile).order_by('date', 'time')
        no_profile_found = False
    except Patient.DoesNotExist:
        appointments = []
        no_profile_found = True
    
    return render(request, 'appointments/patient_appointments.html', {
        'appointments': appointments,
        'no_profile_found': no_profile_found,
    })


@login_required
@permission_required_for('view_own_appointments')
def request_appointment_cancellation(request, appointment_id):
    """Safely triggers an internal status update to request cancellation of an appointment."""
    patient_profile = get_object_or_404(
        Patient, 
        first_name__iexact=request.user.first_name, 
        last_name__iexact=request.user.last_name
    )
    
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient_profile)
    
    if request.method == 'POST':
        appointment.status = 'CANCEL_REQUESTED'
        appointment.save()
        messages.success(request, "Your appointment cancellation request has been submitted successfully.")
        return redirect('patient_appointments_dashboard')
        
    return render(request, 'appointments/confirm_cancel_request.html', {
        'appointment': appointment
    })


@login_required
@permission_required_for('manage_staff')
def generate_reports(request):
    """Filter appointment fields dynamically and export a structured Excel report workbook."""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status_filter = request.GET.get('status')
    export_excel = request.GET.get('export') == 'true'

    appointments = Appointment.objects.all().order_by('date', 'time')

    if start_date:
        appointments = appointments.filter(date__gte=start_date)
    if end_date:
        appointments = appointments.filter(date__lte=end_date)
    if status_filter:
        if status_filter == 'CHECKED_IN':
            appointments = appointments.filter(is_checked_in=True)
        elif status_filter == 'NOT_CHECKED_IN':
            appointments = appointments.filter(is_checked_in=False)
        elif status_filter in ['CANCEL_REQUESTED', 'CANCELLED', 'SCHEDULED']:
            appointments = appointments.filter(status=status_filter)

    if export_excel:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Filtered Appointment Report"

        header_font = openpyxl.styles.Font(name="Times New Roman", size=11, bold=True, color="FFFFFF")
        header_fill = openpyxl.styles.PatternFill(start_color="B05882", end_color="B05882", fill_type="solid")
        data_font = openpyxl.styles.Font(name="Times New Roman", size=11)

        headers = ["Appointment ID", "Patient Name", "Doctor User", "Date Scheduled", "Time Slot", "Checked In", "Status"]
        ws.append(headers)

        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill

        for appt in appointments:
            row = [
                appt.id,
                f"{appt.patient.first_name} {appt.patient.last_name}",
                appt.doctor.get_full_name() if hasattr(appt.doctor, 'get_full_name') else appt.doctor.username,
                appt.date.strftime("%Y-%m-%d") if appt.date else "",
                appt.time.strftime("%I:%M %p") if appt.time else "",
                "Yes" if appt.is_checked_in else "No",
                appt.get_status_display() if hasattr(appt, 'get_status_display') else getattr(appt, 'status', 'SCHEDULED')
            ]
            ws.append(row)

        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=7):
            for cell in row:
                cell.font = data_font

        for col in ws.iter_cols(min_row=1, max_row=ws.max_row, min_col=1, max_col=7):
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)


        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="Hospital_Report.xlsx"'
        wb.save(response)
        return response

    return render(request, 'appointments/generate_report.html', {
        'appointments': appointments,
        'start_date': start_date,
        'end_date': end_date,
        'status': status_filter,
    })
