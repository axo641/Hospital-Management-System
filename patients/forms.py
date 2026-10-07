from django import forms
from .models import Patient

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'address', 'phone_number', 'email', 'medical_history']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
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