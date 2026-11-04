from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Patient, MedicalRecord, TestResult, Invoice, EmergencyContact, Room, AuditLog
from .forms import PatientRegistrationForm, MedicalRecordForm, PatientUpdateForm, TestResultForm, EmergencyContactForm, RoomForm, PatientDocumentForm
from accounts.permissions import permission_required_for, has_permission
from django.core.exceptions import PermissionDenied
from django.utils import timezone

@login_required
@permission_required_for('search_patient')
def search_patients(request):
    """Search patients - all permitted roles can search"""
    query = request.GET.get('q', '')
    patients = []

    if query:
        patients = Patient.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(id__icontains=query)
        )

    return render(request, 'patients/patient_search.html', {
        'patients': patients,
        'query': query,
        'can_edit_patient': has_permission(request.user, 'edit_patient'),
        'can_enter_results': has_permission(request.user, 'enter_test_results'),
    })

@login_required
@permission_required_for('register_patient')
def register_patient(request):
    """Register a new patient and their emergency contact"""
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        emergency_form = EmergencyContactForm(request.POST)
        
        if form.is_valid() and emergency_form.is_valid():
            patient = form.save()
            
            contact = emergency_form.save(commit=False)
            contact.patient = patient
            contact.save()
            
            # --- AUDIT LOG ENTRY ---
            AuditLog.objects.create(
                user=request.user,
                action="Registered Patient",
                details=f"Created patient file for {patient.first_name} {patient.last_name} (ID: {patient.id})"
            )
            
            messages.success(request, "Patient and emergency contact registered successfully.")
            return redirect('patient_search')
    else:
        form = PatientRegistrationForm()
        emergency_form = EmergencyContactForm()

    return render(request, 'patients/register_patient.html', {
        'form': form,
        'emergency_form': emergency_form,
    })

@login_required
@permission_required_for('view_medical_records')
def medical_records_list(request):
    """Display list of all patients for viewing medical records"""
    patients = Patient.objects.all().order_by('first_name', 'last_name')
    return render(request, 'patients/medical_records_list.html', {'patients': patients})

@login_required
@permission_required_for('view_medical_records')
def patient_medical_records(request, patient_id):
    """Display all medical records for a specific patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    medical_records = patient.medical_records.all()
    
    return render(request, 'patients/patient_medical_records.html', {
        'patient': patient,
        'medical_records': medical_records,
    })

@login_required
@permission_required_for('view_medical_records')
def add_medical_record(request, patient_id):
    """Add a new medical record for a patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.save()
            return redirect('patient_medical_records', patient_id=patient.id)
    else:
        form = MedicalRecordForm()

    return render(request, 'patients/add_medical_record.html', {
        'form': form,
        'patient': patient,
    })

@login_required
@permission_required_for('view_medical_records')
def delete_medical_record(request, record_id):
    """Delete a medical record"""
    medical_record = get_object_or_404(MedicalRecord, id=record_id)
    patient_id = medical_record.patient.id
    
    if request.method == 'POST':
        medical_record.delete()
        return redirect('patient_medical_records', patient_id=patient_id)
    
    return render(request, 'patients/delete_medical_record.html', {
        'medical_record': medical_record,
    })

@login_required
@permission_required_for('edit_patient')
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    emergency_contact, created = EmergencyContact.objects.get_or_create(patient=patient)
    
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=patient)
        emergency_form = EmergencyContactForm(request.POST, instance=emergency_contact)
        
        if form.is_valid() and emergency_form.is_valid():
            form.save()
            
            contact = emergency_form.save(commit=False)
            contact.patient = patient
            contact.save()
            
            # --- AUDIT LOG ENTRY ---
            AuditLog.objects.create(
                user=request.user,
                action="Updated Patient",
                details=f"Updated patient file for {patient.first_name} {patient.last_name} (ID: {patient.id})"
            )
            
            messages.success(request, "Patient information and emergency contact updated successfully.")
            return redirect('patient_search')
    else:
        form = PatientUpdateForm(instance=patient)
        emergency_form = EmergencyContactForm(instance=emergency_contact)

    return render(request, 'patients/edit_patient.html', {
        'form': form,
        'emergency_form': emergency_form,
        'patient': patient,
    })

@login_required
@permission_required_for('enter_test_results')
def enter_test_results(request, patient_id):
    """View and submit lab diagnostic entries for a specified patient Profile"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = TestResultForm(request.POST)
        if form.is_valid():
            test_result = form.save(commit=False)
            test_result.patient = patient
            test_result.save()
            
            messages.success(request, f"Test results saved for {patient}.")
            return redirect('enter_test_results', patient_id=patient.id)
    else:
        form = TestResultForm()
        
    previous_tests = patient.test_results.all().order_by('-date_performed')

    context = {
        'patient': patient,
        'form': form,
        'previous_tests': previous_tests,
    }
    return render(request, 'patients/enter_results.html', context)

@login_required
def invoice_list(request):
    """SO-44: Display patient invoices for administrators."""
    if request.user.role != 'ADMIN':
        raise PermissionDenied

    invoices = Invoice.objects.select_related('patient').order_by(
        '-issued_date', '-id'
    )

    return render(request, 'patients/invoice_list.html', {
        'invoices': invoices,
    })

@login_required
def mark_invoice_paid(request, invoice_id):
    if request.user.role != 'ADMIN':
        raise PermissionDenied

    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method != 'POST':
        return redirect('invoice_list')

    if invoice.payment_status == Invoice.PaymentStatus.PAID:
        messages.info(request, "This invoice is already marked as paid.")
    else:
        invoice.payment_status = Invoice.PaymentStatus.PAID
        invoice.paid_at = timezone.now()
        invoice.save(update_fields=['payment_status', 'paid_at'])

        messages.success(
            request,
            f"Invoice #{invoice.id} has been successfully marked as paid."
        )

    return redirect('invoice_list')


@login_required
def room_availability(request):
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    
    rooms = Room.objects.all().order_by('room_number')
    
    if status_filter:
        rooms = rooms.filter(status=status_filter)
    if type_filter:
        rooms = rooms.filter(room_type=type_filter)

    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status=Room.RoomStatus.AVAILABLE).count()
    occupied_rooms = Room.objects.filter(status=Room.RoomStatus.OCCUPIED).count()
    maintenance_rooms = Room.objects.filter(status=Room.RoomStatus.MAINTENANCE).count()

    context = {
        'rooms': rooms,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'maintenance_rooms': maintenance_rooms,
        'selected_status': status_filter,
        'selected_type': type_filter,
        'room_types': Room.RoomType.choices,
        'room_statuses': Room.RoomStatus.choices,
    }
    return render(request, 'patients/room_availability.html', context)

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            
            # --- AUDIT LOG ENTRY ---
            AuditLog.objects.create(
                user=request.user,
                action="Added Room",
                details=f"Added Room {room.room_number} ({room.get_room_type_display()})"
            )
            
            messages.success(request, "New room added successfully.")
            return redirect('room_availability')
    else:
        form = RoomForm()

    return render(request, 'patients/add_room.html', {
        'form': form,
    })

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            
            AuditLog.objects.create(
                user=request.user,
                action="Updated Room",
                details=f"Updated Room {room.room_number} - Status: {room.get_status_display()}"
            )
            
            messages.success(request, f"Room {room.room_number} updated successfully.")
            return redirect('room_availability')
    else:
        form = RoomForm(instance=room)

    return render(request, 'patients/edit_room.html', {
        'form': form,
        'room': room,
    })

@login_required
def audit_logs_view(request):
    logs = AuditLog.objects.all()[:150]
    return render(request, 'patients/audit_logs.html', {
        'logs': logs,
    })

@login_required
def upload_patient_document(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PatientDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient = patient
            document.uploaded_by = request.user
            document.save()
            
            AuditLog.objects.create(
                user=request.user,
                action="Uploaded Patient Document",
                details=f"Uploaded document '{document.title}' for patient {patient.first_name} {patient.last_name} (ID: {patient.id})"
            )
            
            messages.success(request, f"Document '{document.title}' uploaded successfully.")
            return redirect('patient_documents_list', patient_id=patient.id)
    else:
        form = PatientDocumentForm()

    return render(request, 'patients/upload_document.html', {
        'form': form,
        'patient': patient,
    })

@login_required
def patient_documents_list(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    documents = patient.documents.all()
    
    return render(request, 'patients/patient_documents.html', {
        'patient': patient,
        'documents': documents,
    })