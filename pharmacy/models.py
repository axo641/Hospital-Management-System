from django.db import models
from django.contrib.auth import get_user_model
from visits.models import PatientVisit

User = get_user_model()


class Medication(models.Model):
    """Catalog of standard medications with default dosages and use instructions (SO-37)."""
    name = models.CharField(max_length=200, unique=True)
    default_dosage = models.CharField(max_length=100, help_text="e.g., 500mg, 10ml, 1 tablet")
    default_instructions = models.TextField(help_text="e.g., Take twice daily after meals for 7 days")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.default_dosage})"


class Prescription(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('DISPENSED', 'Dispensed'),
        ('REJECTED', 'Rejected'),
    ]

    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        null=True,
        blank=True
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescriptions'
    )

    patient_name = models.CharField(max_length=150)
    patient_id_number = models.CharField(max_length=50)  
    doctor_name = models.CharField(max_length=150)
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)           
    instructions = models.TextField()                  
    date_prescribed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    pharmacist_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_prescribed']

    def __str__(self):
        return f"{self.medication_name} for {self.patient_name} ({self.status})"