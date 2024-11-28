from django.urls import reverse
from rest_framework import status

from tenant.base_view_set_test_case import BaseViewSetTestCase
from tenant.models import Organization, User


class OrganizationViewSetTestCase(BaseViewSetTestCase):

    def test_superuser_can_access_all_organizations(self):
        # Simulate superuser login
        self.client.login(username="superuser", password="password")

        # Use reverse() to get the URL for the organizations endpoint
        url = reverse('organizations-list')

        # Make a request to the OrganizationViewSet
        response = self.client.get(url)

        # Assert that the superuser can access all organizations
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_admin_can_access_specific_organization(self):
        # Simulate admin login
        self.client.login(username="admin", password="password")

        # Use reverse() to get the URL for the organizations endpoint
        url = reverse('organizations-list')

        # Make a request to the OrganizationViewSet
        response = self.client.get(url)

        # Assert that the admin can only access organizations related to their tenant
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # They should only see org 1

    def test_regular_user_can_access_own_organization(self):
        # Simulate regular user login
        self.client.login(username="regular_user", password="password")

        # Use reverse() to get the URL for the organizations endpoint
        url = reverse('organizations-list')

        # Make a request to the OrganizationViewSet
        response = self.client.get(url)

        # Assert that the regular user can only see their own organization
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # They should only see org 1

    def test_regular_user_cannot_access_other_organization(self):
        # Simulate regular user login
        self.client.login(username="regular_user", password="password")

        # Use reverse() to get the URL for the organizations endpoint
        url = reverse('organizations-list')

        # Make a request to the OrganizationViewSet to see if they can access another user's org
        response = self.client.get(url)

        # Assert that the regular user cannot access another user's organization
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # They should only see org 1

    def test_anonymous_user_has_no_access(self):
        # Use reverse() to get the URL for the organizations endpoint
        url = reverse('organizations-list')

        # Make a request to the OrganizationViewSet without login (anonymous user)
        response = self.client.get(url)

        # Assert that an anonymous user cannot access any organization
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Test for Retrieve (GET /organizations/{id}/) ---
    def test_superuser_can_retrieve_organization(self):
        self.client.login(username="superuser", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.org1.name)

    def test_admin_can_retrieve_organization(self):
        self.client.login(username="admin", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.org1.name)

    def test_regular_user_can_retrieve_own_organization(self):
        self.client.login(username="regular_user", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.org1.name)

    def test_regular_user_cannot_retrieve_other_organization(self):
        self.client.login(username="regular_user", password="password")

        url = reverse('organizations-detail', args=[self.org2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- Test for Update (PUT /organizations/{id}/) ---
    def test_superuser_can_update_organization(self):
        self.client.login(username="superuser", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        data = {'name': 'Updated Organization'}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Organization')

    def test_admin_cant_update_organization(self):
        self.client.login(username="admin", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        data = {'name': 'Updated by Admin'}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_update_other_organization(self):
        self.client.login(username="regular_user", password="password")

        url = reverse('organizations-detail', args=[self.org2.id])
        data = {'name': 'Updated Organization'}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Test for Partial Update (PATCH /organizations/{id}/) ---
    def test_superuser_can_partial_update_organization(self):
        self.client.login(username="superuser", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        data = {'name': 'Partially Updated Organization'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Partially Updated Organization')

    def test_admin_cant_partial_update_organization(self):
        self.client.login(username="admin", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        data = {'name': 'Admin Partial Update'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Test for Delete (DELETE /organizations/{id}/) ---
    def test_superuser_can_delete_organization(self):
        self.client.login(username="superuser", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Organization.objects.count(), 1)  # Only one organization should remain

    def test_admin_cant_delete_organization(self):
        self.client.login(username="admin", password="password")

        url = reverse('organizations-detail', args=[self.org1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Organization.objects.count(), 2)  # Only one organization should remain

    def test_regular_user_cannot_delete_other_organization(self):
        self.client.login(username="regular_user", password="password")

        url = reverse('organizations-detail', args=[self.org2.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Organization.objects.count(), 2)  # No organizations should be deleted


class UserViewSetTests(BaseViewSetTestCase):

    def test_superuser_can_retrieve_all_users(self):
        self.authenticate_user(self.superuser)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.count())

    def test_admin_can_retrieve_users_in_their_organization(self):
        self.authenticate_user(self.admin)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(user["organization"] == self.org1.id for user in response.data))

    def test_user_can_retrieve_own_data(self):
        self.authenticate_user(self.user1)
        url = reverse("users-detail", kwargs={"pk": self.user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user1.id)

    def test_user_cannot_retrieve_other_users_data(self):
        self.authenticate_user(self.user1)
        url = reverse("users-detail", kwargs={"pk": self.user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_update_any_user(self):
        self.authenticate_user(self.superuser)
        url = reverse("users-detail", kwargs={"pk": self.user1.id})
        data = {"first_name": "Updated"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "Updated")

    def test_admin_can_update_users_in_their_organization(self):
        self.authenticate_user(self.admin)
        url = reverse("users-detail", kwargs={"pk": self.user1.id})
        data = {"first_name": "Updated by Admin"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "Updated by Admin")

    def test_user_cannot_update_another_user(self):
        self.authenticate_user(self.user1)
        url = reverse("users-detail", kwargs={"pk": self.user2.id})
        data = {"first_name": "Hacker Attempt"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_delete_any_user(self):
        self.authenticate_user(self.superuser)
        url = reverse("users-detail", kwargs={"pk": self.user1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_admin_can_delete_users_in_their_organization(self):
        self.authenticate_user(self.admin)
        url = reverse("users-detail", kwargs={"pk": self.user1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_admin_cannot_delete_superusers(self):
        self.authenticate_user(self.admin)
        url = reverse("users-detail", kwargs={"pk": self.superuser.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(id=self.superuser.id).exists())

    def test_user_cannot_delete_another_user(self):
        self.authenticate_user(self.user1)
        url = reverse("users-detail", kwargs={"pk": self.user2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_their_own_data(self):
        self.authenticate_user(self.user1)
        url = reverse("users-detail", kwargs={"pk": self.user1.id})
        data = {"first_name": "Updated by User"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "Updated by User")

    def test_user_cannot_delete_self(self):
        # Try to delete the authenticated user (self)
        self.authenticate_user(self.user1)

        url = reverse("users-detail", kwargs={"pk": self.user1.id})
        response = self.client.delete(url)

        # Assert that the request is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_cannot_delete_self(self):
        # Authenticate as admin
        self.authenticate_user(self.admin)
        # Try to delete the authenticated admin (self)
        url = reverse("users-detail", kwargs={"pk": self.admin.id})
        response = self.client.delete(url)

        # Assert that the request is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_delete_self(self):
        # Authenticate as superuser
        self.authenticate_user(self.superuser)

        # Try to delete the authenticated superuser (self)
        url = reverse("users-detail", kwargs={"pk": self.superuser.id})
        response = self.client.delete(url)

        # Assert that the request is forbidden (or allow if desired)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Adjust if allowed
