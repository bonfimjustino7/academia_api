from django.urls import path
from rest_framework import routers

from api.viewsets.academia import AcademiaViewSet
from api.viewsets.aluno import AlunoViewSet

from api.viewsets.auth import AuthToken

router = routers.SimpleRouter()
router.register(r'academia', AcademiaViewSet)
router.register(r'aluno', AlunoViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('auth/', AuthToken.as_view())
]