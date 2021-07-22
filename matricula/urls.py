from rest_framework_nested import routers

from .api.viewsets import MatriculaViewSet, MensalidadeViewSet

router = routers.SimpleRouter()
router.register(r'matricula', MatriculaViewSet, basename='matricula')

nested_routes = routers.NestedSimpleRouter(router, 'matricula', lookup='matricula')
nested_routes.register('mensalidades', MensalidadeViewSet, basename='mensalidades')


urlpatterns = router.urls + nested_routes.urls
