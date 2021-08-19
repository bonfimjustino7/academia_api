from django.db.models import Q
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from .permissions import IsAlunoPermission
from .serializers import AlunoSerializer, AlunoSerializerInput, AlunoSerializerUpdateInput, \
    AlunoChangePasswordSerialser, MedicoesSerializer
from ..models import Aluno


class AlunoViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    permission_classes = [IsAlunoPermission]
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return AlunoSerializerUpdateInput
        elif self.action == 'create':
            return AlunoSerializerInput
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return []
        return super(AlunoViewSet, self).get_permissions()

    def update(self, request, *args, **kwargs):
        super(AlunoViewSet, self).update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = AlunoSerializer(instance=instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], url_name='medicoes', url_path='medicoes')
    def medicoes(self, request, *args, **kwargs):
        aluno = self.get_object()
        if request.method == 'POST':
            serializer = MedicoesSerializer(data={**request.data, 'aluno': aluno.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'results': 'Medições Salvas'})
        else:
            if hasattr(aluno, 'medicoes'):
                serializer = MedicoesSerializer(aluno.medicoes.all(), many=True)
                return Response({'medicoes': serializer.data})
            return Response({'medicoes': None})

    @action(detail=True, methods=['patch'], url_name='change_password', url_path='change_password')
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AlunoChangePasswordSerialser(instance=instance, data=request.data,
                                                     partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response({'result': 'Senha alterada'})