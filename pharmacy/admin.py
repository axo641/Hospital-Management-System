from django.contrib import admin
from .models import Medication, Prescription

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_dosage', 'is_active')
    search_fields = ('name', 'default_dosage', 'default_instructions')
    list_filter = ('is_active',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'dosage', 'patient_name', 'doctor_name', 'status', 'date_prescribed')
    list_filter = ('status', 'date_prescribed')
    search_fields = ('medication_name', 'patient_name', 'patient_id_number', 'doctor_name')