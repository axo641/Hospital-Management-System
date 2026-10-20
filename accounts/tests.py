from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import TestCase, RequestFactory

from .permissions import has_permission, permission_required_for


class RolePermissionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.receptionist = User.objects.create_user(
            'rec', password='pw12345!', role='RECEPTIONIST')
        self.physician = User.objects.create_user(
            'doc', password='pw12345!', role='PHYSICIAN')
        self.factory = RequestFactory()

    def test_receptionist_can_register_patients(self):
        self.assertTrue(has_permission(self.receptionist, 'register_patient'))

    def test_physician_cannot_register_patients(self):
        self.assertFalse(has_permission(self.physician, 'register_patient'))

    def test_decorator_blocks_wrong_role(self):
        @permission_required_for('register_patient')
        def view(request):
            return HttpResponse('ok')

        request = self.factory.get('/')
        request.user = self.physician
        with self.assertRaises(PermissionDenied):
            view(request)

    def test_decorator_allows_right_role(self):
        @permission_required_for('register_patient')
        def view(request):
            return HttpResponse('ok')

        request = self.factory.get('/')
        request.user = self.receptionist
        self.assertEqual(view(request).status_code, 200)