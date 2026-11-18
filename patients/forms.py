from django import forms
from .models import Patient, MedicalRecord, TestResult, Invoice, EmergencyContact, Room, PatientDocument


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'address', 'phone_number', 'email', 'medical_history', 'allergies']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        first = cleaned.get('first_name')
        last = cleaned.get('last_name')
        dob = cleaned.get('date_of_birth')
        email = cleaned.get('email')

        if first and last and dob:
            if Patient.objects.filter(
                first_name__iexact=first,
                last_name__iexact=last,
                date_of_birth=dob,
            ).exists():
                raise forms.ValidationError(
                    "A patient file already exists for this name and date of birth."
                )

        if email and Patient.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A patient already exists with this email address."
            )

        return cleaned


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone_number', 'email']
        labels = {
            'name': 'Contact Name',
            'relationship': 'Relationship to Patient',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Removes small helper text underneath inputs
        for field in self.fields.values():
            field.help_text = None


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['title', 'description', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'address', 'phone_number', 'email', 'medical_history', 'allergies']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        first = cleaned.get('first_name')
        last = cleaned.get('last_name')
        dob = cleaned.get('date_of_birth')
        email = cleaned.get('email')
        other_patients = Patient.objects.exclude(pk=self.instance.pk)

        if first and last and dob:
            if other_patients.filter(
                first_name__iexact=first,
                last_name__iexact=last,
                date_of_birth=dob,
            ).exists():
                raise forms.ValidationError(
                    "A patient file already exists for this name and date of birth."
                )

        if email and other_patients.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A patient already exists with this email address."
            )

        return cleaned


class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['test_type', 'results', 'date_performed']
        widgets = {
            'test_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Complete Blood Count'}),
            'results': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter results details...'}),
            'date_performed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'status', 'capacity', 'assigned_patient']
        labels = {
            'room_number': 'Room Number',
            'room_type': 'Room Type',
            'status': 'Room Status',
            'capacity': 'Capacity',
            'assigned_patient': 'Assigned Patient',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
        self.fields['assigned_patient'].queryset = Patient.objects.all().order_by('last_name', 'first_name')
        self.fields['assigned_patient'].required = False

class PatientDocumentForm(forms.ModelForm):
    class Meta:
        model = PatientDocument
        fields = ['title', 'file']
        labels = {
            'title': 'Short Description',
            'file': 'Select File',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None