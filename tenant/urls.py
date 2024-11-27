from rest_framework import routers

from tenant import views

router = routers.SimpleRouter()
router.register(r'organizations', views.OrganizationViewSet, basename='organizations')
router.register(r'users', views.UserViewSet, basename='users')
urlpatterns = router.urls
