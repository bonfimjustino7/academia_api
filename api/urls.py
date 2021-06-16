from rest_framework import routers

from api.viewsets.academia import AcademiaViewSet

router = routers.SimpleRouter()
router.register(r'academia', AcademiaViewSet)

urlpatterns = router.urls