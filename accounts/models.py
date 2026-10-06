from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        # add the rest of the SO-8 role titles here

    role = models.CharField(max_length=20, choices=Role.choices)
