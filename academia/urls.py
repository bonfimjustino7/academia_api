from rest_framework_nested import routers

from .api.viewsets import AcademiaViewSet

router = routers.SimpleRouter()
router.register(r'academia', AcademiaViewSet, basename='academia')

urlpatterns = router.urls
