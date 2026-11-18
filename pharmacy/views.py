import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from visits.models import PatientVisit
from .models import Prescription, Medication
from .forms import PrescriptionReviewForm, PrescriptionForm, VisitPrescriptionForm


@login_required
def prescription_list_view(request):
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    prescriptions = Prescription.objects.all()

    if status_filter:
        prescriptions = prescriptions.filter(status=status_filter)

    if search_query:
        prescriptions = prescriptions.filter(
            Q(patient_name__icontains=search_query) |
            Q(patient_id_number__icontains=search_query) |
            Q(medication_name__icontains=search_query)
        )

    context = {
        'prescriptions': prescriptions,
        'current_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'pharmacist_prescriptions.html', context)


@login_required
def prescription_detail_view(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    
    if request.method == 'POST':
        form = PrescriptionReviewForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:pharmacist_prescriptions')
    else:
        form = PrescriptionReviewForm(instance=prescription)

    context = {
        'prescription': prescription,
        'form': form,
    }
    return render(request, 'pharmacist_prescription_detail.html', context)


@login_required
def prescription_create_view(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            selected_patient = form.cleaned_data['patient_select']
            
            # Automatically populate patient fields from the selected Patient model instance
            prescription.patient_name = str(selected_patient)
            prescription.patient_id_number = getattr(selected_patient, 'patient_id', str(selected_patient.pk))
            
            prescription.save()
            return redirect('pharmacy:pharmacist_prescriptions')
    else:
        form = PrescriptionForm()

    context = {
        'form': form,
    }
    return render(request, 'prescription_form.html', context)


@login_required
def prescribe_for_visit_view(request, visit_pk):
    user_role = getattr(request.user, 'role', '')
    if user_role not in ['PHYSICIAN', 'SURGEON'] and not request.user.is_superuser and user_role != 'ADMIN':
        raise PermissionDenied

    visit = get_object_or_404(PatientVisit, pk=visit_pk)
    patient = visit.patient

    # Serialize active medications from SO-37 so the UI can auto-fill dosage & instructions
    medications = Medication.objects.filter(is_active=True)
    med_catalog = {
        str(med.pk): {
            'name': med.name,
            'dosage': med.default_dosage,
            'instructions': med.default_instructions,
        }
        for med in medications
    }

    if request.method == 'POST':
        form = VisitPrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.visit = visit
            prescription.medication = form.cleaned_data.get('medication_select')
            prescription.patient_name = str(patient)
            prescription.patient_id_number = getattr(patient, 'patient_id', str(patient.pk))
            if not prescription.doctor_name:
                prescription.doctor_name = visit.doctor_name or f"Dr. {request.user.get_full_name() or request.user.username}"
            prescription.save()
            return redirect('visits:patient_history', patient_pk=patient.pk)
    else:
        initial_data = {
            'doctor_name': visit.doctor_name or f"Dr. {request.user.get_full_name() or request.user.username}",
            'medication_name': '',
            'dosage': '',
            'instructions': '',
        }
        form = VisitPrescriptionForm(initial=initial_data)

    return render(request, 'prescribe_visit_medication.html', {
        'form': form,
        'visit': visit,
        'patient': patient,
        'med_catalog_json': json.dumps(med_catalog),
    })


@login_required
def print_prescription_view(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'print_prescription.html', {
        'prescription': prescription,
    })


@login_required
def patient_prescriptions_view(request):
    user_query = request.user.username
    full_name = request.user.get_full_name()
    
    prescriptions = Prescription.objects.filter(
        Q(patient_name__icontains=user_query) | 
        Q(patient_name__icontains=full_name)
    )

    context = {
        'prescriptions': prescriptions,
    }
    return render(request, 'patient_prescriptions.html', context)