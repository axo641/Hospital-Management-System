from django import forms
from .models import Prescription
from patients.models import Patient
from .models import Medication

class PrescriptionReviewForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['status', 'pharmacist_notes']
        widgets = {
            'status': forms.Select(attrs={
                'style': 'padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-family: "Times New Roman", Times, serif; font-size: 15px; width: 100%;'
            }),
            'pharmacist_notes': forms.Textarea(attrs={
                'style': 'padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-family: "Times New Roman", Times, serif; font-size: 15px; width: 100%; resize: vertical; height: 100px;',
                'placeholder': 'Enter dosage verification notes, safety checks, or pickup instructions...'
            }),
        }

class PrescriptionForm(forms.ModelForm):
    patient_select = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label="Select Patient",
        required=True,
        widget=forms.Select(attrs={
            'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'
        })
    )

    class Meta:
        model = Prescription
        fields = ['patient_select', 'doctor_name', 'medication_name', 'dosage', 'instructions']
        widgets = {
            'doctor_name': forms.TextInput(attrs={'placeholder': 'Prescribing doctor name', 'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'}),
            'medication_name': forms.TextInput(attrs={'placeholder': 'Medication name', 'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'}),
            'dosage': forms.TextInput(attrs={'placeholder': 'e.g., 500mg, 1 tablet twice daily', 'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Detailed administration instructions...', 'style': 'padding: 10px; width: 100%; height: 80px; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; resize: vertical;'}),
        }

class VisitPrescriptionForm(forms.ModelForm):
    medication_select = forms.ModelChoiceField(
        queryset=Medication.objects.filter(is_active=True),
        required=False,
        empty_label="-- Select from Medication Database (or enter manually below) --",
        label="Medication Catalog (Auto-fills Dosage & Instructions)",
        widget=forms.Select(attrs={
            'id': 'id_medication_select',
            'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'
        })
    )

    class Meta:
        model = Prescription
        fields = ['doctor_name', 'medication_name', 'dosage', 'instructions']
        widgets = {
            'doctor_name': forms.TextInput(attrs={
                'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'
            }),
            'medication_name': forms.TextInput(attrs={
                'id': 'id_medication_name',
                'placeholder': 'e.g., Amoxicillin 500mg',
                'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'
            }),
            'dosage': forms.TextInput(attrs={
                'id': 'id_dosage',
                'placeholder': 'e.g., 500mg / 1 capsule',
                'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'
            }),
            'instructions': forms.Textarea(attrs={
                'id': 'id_instructions',
                'rows': 4,
                'placeholder': 'e.g., Take 1 capsule by mouth three times daily for 7 days with food.',
                'style': 'padding: 10px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; resize: vertical;'
            }),
        }