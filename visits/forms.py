from django import forms
from .models import PatientVisit

class PatientVisitForm(forms.ModelForm):
    class Meta:
        model = PatientVisit
        fields = ['appointment', 'doctor_name', 'diagnosis', 'treatment_notes']
        widgets = {
            'appointment': forms.Select(attrs={
                'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'
            }),
            'doctor_name': forms.TextInput(attrs={
                'placeholder': 'Dr. Lastname / Treating Physician',
                'style': 'padding: 8px; width: 100%; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px;'
            }),
            'diagnosis': forms.Textarea(attrs={
                'placeholder': 'Enter primary diagnosis...',
                'style': 'padding: 10px; width: 100%; height: 80px; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; resize: vertical;'
            }),
            'treatment_notes': forms.Textarea(attrs={
                'placeholder': 'Enter treatment administered, prescriptions given, and follow-up care...',
                'style': 'padding: 10px; width: 100%; height: 100px; font-family: "Times New Roman", Times, serif; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; resize: vertical;'
            }),
        }