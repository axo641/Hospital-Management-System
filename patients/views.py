from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Patient, MedicalRecord, TestResult
from .forms import PatientRegistrationForm, MedicalRecordForm, PatientUpdateForm, TestResultForm
from accounts.permissions import permission_required_for, has_permission


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
        'can_enter_results': has_permission(request.user, 'enter_test_results'),  # Added context permission
    })


@login_required
@permission_required_for('register_patient')
def register_patient(request):
    """Register a new patient - only users with permission can do this"""
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_search')
    else:
        form = PatientRegistrationForm()

    return render(request, 'patients/register_patient.html', {'form': form})


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
    
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_search')
    else:
        form = PatientUpdateForm(instance=patient)

    return render(request, 'patients/edit_patient.html', {
        'form': form,
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
            # Create object but don't commit to DB yet so we can attach the patient
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
