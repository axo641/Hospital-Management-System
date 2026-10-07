from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientRegistrationForm
from accounts.permissions import permission_required_for


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
        'query': query
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
