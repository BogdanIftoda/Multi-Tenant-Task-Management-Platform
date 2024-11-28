from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.filters import TaskFilter
from project.models import Project, Task, Label
from project.permissions import IsAdminOrReadOnly
from project.serializers import ProjectWriteSerializer, ProjectReadSerializer, TaskReadSerializer, TaskWriteSerializer, \
    LabelSerializer
from tenant.custom_view_set import CustomViewSet
from tenant.tenant_filter_decorator import filter_by_role_and_organization


class CustomViewSetWithFilters(CustomViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter


class ProjectViewSet(CustomViewSetWithFilters):

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


class TaskViewSet(CustomViewSetWithFilters):

    def get_queryset(self):
        return Task.objects.prefetch_related("assigned_to").all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TaskWriteSerializer
        return TaskReadSerializer


class LabelViewSet(CustomViewSet):
    serializer_class = LabelSerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    @filter_by_role_and_organization
    def get_queryset(self):
        return Label.objects.all()
