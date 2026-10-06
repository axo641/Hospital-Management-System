from djando.contrib.auth.forms import UserCreationForm
from .models import User

class StaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')