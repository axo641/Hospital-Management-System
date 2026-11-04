from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Prescription
from .forms import PrescriptionReviewForm, PrescriptionForm

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
def patient_prescriptions_view(request):
    prescriptions = Prescription.objects.filter(patient_name__icontains=request.user.username)

    context = {
        'prescriptions': prescriptions,
    }
    return render(request, 'patient_prescriptions.html', context)

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