from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

from .models import Patient, AuditLog


class Sprint4SecurityTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.doctor = User.objects.create_user(
            username="doctor_test",
            password="TestPassword123!",
            email="doctor@example.com",
            role="PHYSICIAN"
        )

        self.clerk = User.objects.create_user(
            username="clerk_test",
            password="TestPassword123!",
            role="CLERK"
        )

        self.admin = User.objects.create_user(
            username="admin_test",
            password="TestPassword123!",
            role="ADMIN"
        )

        self.patient = Patient.objects.create(
            first_name="Test",
            last_name="Patient",
            date_of_birth=date(2000, 1, 1),
            gender="Other",
            address="Test Address",
            phone_number="1234567890",
            email="patient@example.com"
        )

    def test_doctor_access_is_logged(self):
        self.client.force_login(self.doctor)

        response = self.client.get(
            reverse("patient_medical_records", args=[self.patient.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            AuditLog.objects.filter(
                user=self.doctor,
                action="Viewed Medical Records"
            ).exists()
        )

    def test_clerk_cannot_view_medical_records(self):
        self.client.force_login(self.clerk)

        response = self.client.get(
            reverse("patient_medical_records", args=[self.patient.id])
        )

        self.assertEqual(response.status_code, 403)

    def test_clerk_cannot_view_audit_logs(self):
        self.client.force_login(self.clerk)

        response = self.client.get(reverse("audit_logs"))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_view_audit_logs(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("audit_logs"))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_email(self):
        response = self.client.post(
            reverse("password_reset"),
            {"email": "doctor@example.com"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset/", mail.outbox[0].body)
