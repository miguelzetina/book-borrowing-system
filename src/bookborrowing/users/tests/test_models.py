from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelsTestCase(TestCase):
    """
    Tests for the bookborrowing.users.models module.
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_superuser(
            email='user@email.com',
            password='secret'
        )

    def test_user_model(self):
        email = 'user@email.com'
        user = self.user_model.objects.get(email=email)

        self.assertEqual(user.email, email)
        self.assertEqual(user.role.name, 'superadmin')
        self.assertFalse(user.name)
        self.assertFalse(user.last_name)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertFalse(user.has_admin_permissions)
        self.assertTrue(user.has_superadmin_permissions)
