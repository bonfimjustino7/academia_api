from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from api.serializers.aluno import AlunoSerializer, AlunoSerializerInput
from core.models import Aluno
from rest_framework.response import Response


class AlunoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AlunoSerializerInput
        return self.serializer_class
