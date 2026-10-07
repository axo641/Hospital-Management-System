from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        PHYSICIAN = 'PHYSICIAN', 'Physician'
        SURGEON = 'SURGEON', 'Surgeon'
        NURSE = 'NURSE', 'Nurse'
        PHARMACIST = 'PHARMACIST', 'Pharmacist'
        PHYSIOTHERAPIST = 'PHYSIOTHERAPIST', 'Physiotherapist'
        RADIOLOGIST = 'RADIOLOGIST', 'Radiologist'
        TECHNICIAN = 'TECHNICIAN', 'Technician'
        EXECUTIVE = 'EXECUTIVE', 'Executive'
        CLERK = 'CLERK', 'Clerk'
        OFFICE_ASSISTANT = 'OFFICE_ASSISTANT', 'Office Assistant'

    role = models.CharField(max_length=20, choices=Role.choices, blank=True, null=True)
