from django.db import models
from patients.models import Patient
from appointments.models import Appointment

class PatientVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='visit_records')
    doctor_name = models.CharField(max_length=150)
    diagnosis = models.TextField()
    treatment_notes = models.TextField()
    visit_date = models.DateTimeField(auto_now_add=True)
    # New fields for visit completion and pricing
    visit_price = models.DecimalField(max_digits=10, decimal_places=2, default=150.00)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-visit_date']

    def __str__(self):
        return f"Visit for {self.patient} on {self.visit_date.strftime('%Y-%m-%d %H:%M')}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Invoice Requested'),
        ('GENERATED', 'Generated / Unpaid'),
        ('PAID', 'Paid'),
    ]

    visit = models.OneToOneField(PatientVisit, on_delete=models.CASCADE, related_name='invoice')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visit_invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    notes = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    generated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"Invoice #{self.id} - {self.patient} (${self.amount})"