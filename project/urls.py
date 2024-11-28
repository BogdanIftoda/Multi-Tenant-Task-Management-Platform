from rest_framework import routers

from project import views

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'labels', views.LabelViewSet, basename='label')
urlpatterns = router.urls
