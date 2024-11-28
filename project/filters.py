from django_filters import rest_framework as filters

from project.models import Task


class BaseFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status')
    priority = filters.NumberFilter(field_name='priority')

    class Meta:
        fields = ['status', 'priority']


class TaskFilter(BaseFilter):
    project_id = filters.NumberFilter()
    organization_id = filters.NumberFilter(field_name='project__organization_id')

    class Meta(BaseFilter.Meta):
        model = Task
        fields = ['project_id', 'organization_id']


class ProjectFilter(BaseFilter):
    organization_id = filters.NumberFilter(field_name='organization_id')

    class Meta(BaseFilter.Meta):
        model = Task
        fields = ['project_id', 'organization_id']
