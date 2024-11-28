from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from tenant.custom_view_set import CustomViewSet
from tenant.models import Organization, User
from tenant.permissions import IsOwnerOrAdmin, OrganizationPermission
from tenant.serializers import OrganizationSerializer, UserReadSerializer, UserWriteSerializer
from tenant.tenant_filter_decorator import filter_by_role_and_organization


class OrganizationViewSet(CustomViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = (IsAuthenticated, OrganizationPermission)

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Organization.objects.filter(id=self.request.user.organization_id)
        return Organization.objects.all()


class UserViewSet(CustomViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['organization_id']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return UserWriteSerializer
        return UserReadSerializer

    @filter_by_role_and_organization
    def get_queryset(self):
        return User.objects.all()
