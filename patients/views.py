from django.shortcuts import render
from django.db.models import Q
from .models import Patient

# Create your views here.
# SO-20: Build the backend logic to pull data from the patient 
# database with a searching ability to filter by keyword like first 
# or last name and ID
def search_patients(request):
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