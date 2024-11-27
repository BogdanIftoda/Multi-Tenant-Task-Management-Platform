from project.models import Project
from project.serializers import ProjectSerializer
from tenant.custom_view_set import CustomViewSet


class ProjectViewSet(CustomViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
