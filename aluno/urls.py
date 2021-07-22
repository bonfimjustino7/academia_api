from rest_framework_nested import routers

from .api.viewsets import AlunoViewSet

router = routers.SimpleRouter()
router.register(r'aluno', AlunoViewSet, basename='aluno')

urlpatterns = router.urls