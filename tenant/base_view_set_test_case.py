from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from tenant.models import Role, Organization


class BaseViewSetTestCase(APITestCase):
    def setUp(self):
        # Create roles
        self.role_user = Role.objects.get(name=Role.USER)
        self.role_admin = Role.objects.get(name=Role.ADMIN)
        self.role_superuser = Role.objects.get(name=Role.SUPERUSER)

        # Create organizations
        self.org1 = Organization.objects.create(name="Org 1")
        self.org2 = Organization.objects.create(name="Org 2")

        # Create superuser
        self.superuser = get_user_model().objects.create_user(
            username="superuser",
            first_name="Superuser",
            last_name="Superuser",
            password="password",
            email="superuser@s.com",
            role=self.role_superuser,
            organization=self.org1
        )

        # Create admin user
        self.admin = get_user_model().objects.create_user(
            username="admin",
            first_name="Admin",
            last_name="Admin",
            password="password",
            email="admin@s.com",
            role=self.role_admin,
            organization=self.org1
        )

        # Create regular user
        self.user1 = get_user_model().objects.create_user(
            username="regular_user",
            first_name="Regular user 1",
            last_name="Regular user 1",
            password="password",
            email="regular_user@s.com",
            role=self.role_user,
            organization=self.org1
        )

        # Create a second regular user for testing
        self.user2 = get_user_model().objects.create_user(
            username="regular_user_2",
            first_name="Regular user 2",
            last_name="Regular user 2",
            password="password",
            email="regular_user2@s.com",
            role=self.role_user,
            organization=self.org2
        )

    def authenticate_user(self, user):
        self.client.force_authenticate(user=user)
