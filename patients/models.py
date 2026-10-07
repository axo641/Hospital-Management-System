from django.db import models

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"


class MedicalRecord(models.Model):
    """Store medical record documents/files for patients"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='medical_records/%Y/%m/%d/')
    record_date = models.DateField(auto_now_add=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.title} ({self.uploaded_date.date()})"
