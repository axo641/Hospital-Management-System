from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('DISPENSED', 'Dispensed'),
        ('REJECTED', 'Rejected'),
    ]

    patient_name = models.CharField(max_length=150)
    patient_id_number = models.CharField(max_length=50) # e.g. Patient MRN / ID
    doctor_name = models.CharField(max_length=150)
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)           # e.g., "500mg"
    instructions = models.TextField()                  # e.g., "Take twice daily after meals"
    date_prescribed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    pharmacist_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_prescribed']

    def __str__(self):
        return f"{self.medication_name} for {self.patient_name} ({self.status})"