from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# SO-4: Set-up user accounts database where current users reside 
# and new users can be added 

class CustomUserCreationForm(UserCreationForm):
    # Add an email field to the form, making it a required field
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # Use Django's standard field names: first_name and last_name
        fields = ["first_name", "last_name","username", "email"]
=======
from djando.contrib.auth.forms import UserCreationForm
from .models import User

class StaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')
