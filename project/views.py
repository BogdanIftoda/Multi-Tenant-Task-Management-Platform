from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from project.filters import TaskFilter
from project.models import Project, Task
from project.serializers import ProjectWriteSerializer, ProjectReadSerializer, TaskReadSerializer, TaskWriteSerializer
from tenant.custom_view_set import CustomViewSet
from tenant.tenant_filter_decorator import filter_by_role_and_organization


@swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'organization_id',
            openapi.IN_QUERY,
            description='Filter by Organization ID (via Project)',
            type=openapi.TYPE_INTEGER,
        ),
    ]
)
class ProjectViewSet(CustomViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['organization_id']

    @filter_by_role_and_organization
    def get_queryset(self):
        return Project.objects.prefetch_related("workers").all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ProjectWriteSerializer
        return ProjectReadSerializer

    # @filter_by_role_and_organization
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        tasks = Task.objects.prefetch_related("assigned_to").filter(project_id=self.kwargs['pk'])
        serializer = TaskReadSerializer(tasks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


@swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'project_id',
            openapi.IN_QUERY,
            description='Filter by Project ID',
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            'organization_id',
            openapi.IN_QUERY,
            description='Filter by Organization ID (via Project)',
            type=openapi.TYPE_INTEGER,
        ),
    ]
)
class TaskViewSet(CustomViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TaskWriteSerializer
        return TaskReadSerializer
