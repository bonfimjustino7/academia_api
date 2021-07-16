from rest_framework import routers

from .api.viewsets import AlunoViewSet

router = routers.SimpleRouter()
router.register(r'aluno', AlunoViewSet, basename='aluno')

urlpatterns = router.urls