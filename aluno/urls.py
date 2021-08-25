from rest_framework_nested import routers

from .api.viewsets import AlunoViewSet, MedicoesViewSet

router = routers.SimpleRouter()
router.register(r'aluno', AlunoViewSet, basename='aluno')

nested_routes = routers.NestedSimpleRouter(router, 'aluno', lookup='aluno')
nested_routes.register('medicoes', MedicoesViewSet, basename='medicoes')

urlpatterns = router.urls + nested_routes.urls
