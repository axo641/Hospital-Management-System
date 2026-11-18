from django.db import models
from django.utils import timezone
from django.conf import settings

class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"


class EmergencyContact(models.Model):
    patient = models.OneToOneField(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='emergency_contact'
    )
    name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relationship}) for {self.patient}"


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


class TestResult(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='test_results')
    
    test_type = models.CharField(max_length=100, help_text="e.g., Blood Count, Lipid Panel, X-Ray")
    results = models.TextField(help_text="Enter the raw data, findings, or metrics here.")
    date_performed = models.DateField(default=timezone.now)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_type} for {self.patient.first_name} {self.patient.last_name} on {self.date_performed}"


class Invoice(models.Model):

    class PaymentStatus(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PAID = 'PAID', 'Paid'

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    issued_date = models.DateField(default=timezone.localdate)

    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID
    )

    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.patient} - {self.payment_status}"

class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = 'SINGLE', 'Single Room'
        DOUBLE = 'DOUBLE', 'Double Room'
        ICU = 'ICU', 'ICU'
        SUITE = 'SUITE', 'Suite'
        WARD = 'WARD', 'General Ward'

    class RoomStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        OCCUPIED = 'OCCUPIED', 'Occupied'
        MAINTENANCE = 'MAINTENANCE', 'Under Maintenance'

    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=RoomType.choices, default=RoomType.SINGLE)
    status = models.CharField(max_length=20, choices=RoomStatus.choices, default=RoomStatus.AVAILABLE)
    capacity = models.PositiveIntegerField(default=1)
    assigned_patient = models.ForeignKey(
        Patient, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='assigned_room'
    )

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()}) - {self.get_status_display()}"

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        username = self.user.username if self.user else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {username}: {self.action}"

class PatientDocument(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='patient_documents/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.patient}"