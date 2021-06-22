from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers.aluno import AlunoSerializer
from core.models import Aluno


class AlunoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
