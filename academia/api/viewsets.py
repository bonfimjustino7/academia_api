from django.contrib.auth import get_user_model
from rest_framework.decorators import action

from matricula.models import Matricula
from .serializers import AcademiaSerializer, AcademiaSerializerInput, \
    AcademiaSerializerUpdateInput, AcademiaChangePasswordSerialser
from ..models import Academia
from rest_framework.response import Response
from auth_api.api.viewsets import ModelViewSetOwner

User = get_user_model()


class AcademiaViewSet(ModelViewSetOwner):
    queryset = Academia.objects.all()
    serializer_class = AcademiaSerializer

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return AcademiaSerializerUpdateInput
        elif self.action == 'create':
            return AcademiaSerializerInput
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        super(AcademiaViewSet, self).update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = AcademiaSerializer(instance=instance)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_name='change_password', url_path='change_password')
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AcademiaChangePasswordSerialser(instance=instance, data=request.data,
                                                     partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response({'result': 'Senha alterada'})

    @action(detail=True, methods=['get'], url_name='estatisticas', url_path='estatisticas')
    def estatisticas(self, request, *args, **kwargs):
        academia = self.get_object()
        data = {
            'alunos_ativos': academia.alunos_ativos,
            'alunos_inativos': academia.alunos_inativos,
        }
        return Response(data)
