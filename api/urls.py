from rest_framework import routers

from api.viewsets.academia import AcademiaViewSet

from api.viewsets.auth import AuthToken

router = routers.SimpleRouter()
router.register(r'academia', AcademiaViewSet)
router.register(r'auth', AuthToken)

urlpatterns = router.urls