from django_filters import rest_framework as filters

from project.models import Task


class TaskFilter(filters.FilterSet):
    project_id = filters.NumberFilter()
    organization_id = filters.NumberFilter(field_name='project__organization_id')
    status = filters.CharFilter(field_name='status')
    priority = filters.NumberFilter(field_name='priority')

    class Meta:
        model = Task
        fields = ['project_id', 'organization_id']
