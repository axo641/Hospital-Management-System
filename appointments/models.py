from django.db import models
from django.conf import settings
from patients.models import Patient

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    is_checked_in = models.BooleanField(default=False)
    arrival_time = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CANCEL_REQUESTED', 'Cancellation Requested'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date} {self.time}"