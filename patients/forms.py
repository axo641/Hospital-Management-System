from django import forms
from .models import Patient

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender',
                  'phone', 'email', 'address', 'health_card_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        first = cleaned.get('first_name')
        last = cleaned.get('last_name')
        dob = cleaned.get('date_of_birth')
        hcn = cleaned.get('health_card_number')

        # Duplicate check 1: same name + date of birth
        if first and last and dob:
            if Patient.objects.filter(
                first_name__iexact=first,
                last_name__iexact=last,
                date_of_birth=dob,
            ).exists():
                raise forms.ValidationError(
                    "A patient file already exists for this name and date of birth."
                )

        # Duplicate check 2: same health card number
        if hcn and Patient.objects.filter(health_card_number=hcn).exists():
            raise forms.ValidationError(
                "A patient file already exists with this health card number."
            )

        return cleaned