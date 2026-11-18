from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from patients.models import Patient
from .models import PatientVisit, Invoice
from .forms import PatientVisitForm

@login_required
def patient_history_view(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    visits = patient.visits.all()

    return render(request, 'patient_history.html', {
        'patient': patient,
        'visits': visits,
    })

@login_required
def add_visit_notes_view(request, patient_pk):
    user_role = getattr(request.user, 'role', '')
    if user_role not in ['PHYSICIAN', 'SURGEON'] and not request.user.is_superuser and user_role != 'ADMIN':
        raise PermissionDenied

    patient = get_object_or_404(Patient, pk=patient_pk)

    if request.method == 'POST':
        form = PatientVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            if not visit.doctor_name:
                visit.doctor_name = f"Dr. {request.user.get_full_name() or request.user.username}"
            visit.save()
            return redirect('visits:patient_history', patient_pk=patient.pk)
    else:
        initial_data = {
            'doctor_name': f"Dr. {request.user.get_full_name() or request.user.username}",
            'diagnosis': '',
            'treatment_notes': '',
        }
        form = PatientVisitForm(initial=initial_data)

    return render(request, 'add_visit_notes.html', {
        'form': form,
        'patient': patient,
        'is_edit': False
    })

@login_required
def edit_visit_notes_view(request, visit_pk):
    user_role = getattr(request.user, 'role', '')
    if user_role not in ['PHYSICIAN', 'SURGEON'] and not request.user.is_superuser and user_role != 'ADMIN':
        raise PermissionDenied

    visit = get_object_or_404(PatientVisit, pk=visit_pk)

    if request.method == 'POST':
        form = PatientVisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            return redirect('visits:patient_history', patient_pk=visit.patient.pk)
    else:
        form = PatientVisitForm(instance=visit)

    return render(request, 'add_visit_notes.html', {
        'form': form,
        'patient': visit.patient,
        'visit': visit,
        'is_edit': True
    })

@login_required
def complete_visit_view(request, visit_pk):
    if getattr(request.user, 'role', '') == 'PATIENT':
        raise PermissionDenied

    visit = get_object_or_404(PatientVisit, pk=visit_pk)
    if request.method == 'POST':
        visit.is_completed = True
        visit.save()

        # Automatically request an invoice if one hasn't been requested yet
        Invoice.objects.get_or_create(
            visit=visit,
            defaults={
                'patient': visit.patient,
                'amount': visit.visit_price,
                'status': 'REQUESTED',
            }
        )
    return redirect('visits:patient_history', patient_pk=visit.patient.pk)

@login_required
def admin_billing_dashboard(request):
    """Admin queue for viewing requested invoices and generating bills."""
    if getattr(request.user, 'role', '') != 'ADMIN' and not request.user.is_superuser:
        raise PermissionDenied

    invoices = Invoice.objects.all()
    return render(request, 'admin_billing.html', {
        'invoices': invoices
    })

@login_required
def generate_invoice_view(request, invoice_pk):
    """Admin UI to finalize visit price and generate the official invoice."""
    if getattr(request.user, 'role', '') != 'ADMIN' and not request.user.is_superuser:
        raise PermissionDenied

    invoice = get_object_or_404(Invoice, pk=invoice_pk)

    if request.method == 'POST':
        final_price = request.POST.get('amount')
        billing_notes = request.POST.get('notes', '')
        action = request.POST.get('action', 'GENERATE')

        if final_price:
            invoice.amount = final_price
            invoice.visit.visit_price = final_price
            invoice.visit.save()

        invoice.notes = billing_notes
        if action == 'MARK_PAID':
            invoice.status = 'PAID'
        else:
            invoice.status = 'GENERATED'
            invoice.generated_at = timezone.now()
            
        invoice.save()
        return redirect('visits:admin_billing')

    return render(request, 'generate_invoice.html', {
        'invoice': invoice
    })