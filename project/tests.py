# Create your tests here.
from django.urls import reverse
from rest_framework import status

from project.models import Label
from tenant.base_view_set_test_case import BaseViewSetTestCase


class LabelViewSetTestCase(BaseViewSetTestCase):
    def setUp(self):
        super().setUp()
        # Create some labels for testing
        self.label1 = Label.objects.create(name="Label 1", organization=self.org1)
        self.label2 = Label.objects.create(name="Label 2", organization=self.org2)

    def test_superuser_can_create_label(self):
        self.authenticate_user(self.superuser)
        url = reverse("label-list")
        data = {"name": "New Label", "organization": self.org1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 3)
        self.assertEqual(response.data["name"], "New Label")

    def test_admin_can_create_label(self):
        self.authenticate_user(self.admin)
        url = reverse("label-list")
        data = {"name": "Admin Label", "organization": self.org1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 3)
        self.assertEqual(response.data["name"], "Admin Label")

    def test_user_cannot_create_label(self):
        self.authenticate_user(self.user1)
        url = reverse("label-list")
        data = {"name": "User Label", "organization": self.org1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_update_label(self):
        self.authenticate_user(self.superuser)
        url = reverse("label-detail", kwargs={"pk": self.label1.id})
        data = {"name": "Updated Label"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, "Updated Label")

    def test_admin_can_update_label(self):
        self.authenticate_user(self.admin)
        url = reverse("label-detail", kwargs={"pk": self.label1.id})
        data = {"name": "Admin Updated Label"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, "Admin Updated Label")

    def test_user_cannot_update_label(self):
        self.authenticate_user(self.user1)
        url = reverse("label-detail", kwargs={"pk": self.label1.id})
        data = {"name": "User Updated Label"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_delete_label(self):
        self.authenticate_user(self.superuser)
        url = reverse("label-detail", kwargs={"pk": self.label1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Label.objects.count(), 1)

    def test_admin_can_delete_label(self):
        self.authenticate_user(self.admin)
        url = reverse("label-detail", kwargs={"pk": self.label1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Label.objects.count(), 1)

    def test_user_cannot_delete_label(self):
        self.authenticate_user(self.user1)
        url = reverse("label-detail", kwargs={"pk": self.label1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_list_labels_in_their_organization(self):
        self.authenticate_user(self.user1)
        url = reverse("label-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Label 1")

    def test_user_cannot_list_labels_in_other_organizations(self):
        self.authenticate_user(self.user1)
        url = reverse("label-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        label_names = [label["name"] for label in response.data]
        self.assertNotIn("Label 2", label_names)
