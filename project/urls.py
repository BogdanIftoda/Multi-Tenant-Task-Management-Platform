from rest_framework import routers

from project import views

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
urlpatterns = router.urls
