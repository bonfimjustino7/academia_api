from django.db.models import Q
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from .permissions import IsAlunoPermission, IsMedicoesPermissions
from .serializers import AlunoSerializer, AlunoSerializerInput, AlunoSerializerUpdateInput, \
    AlunoChangePasswordSerialser, MedicoesSerializer
from ..filters import MedicaoFilter
from ..models import Aluno, Medicao


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

    @action(detail=True, methods=['patch'], url_name='change_password', url_path='change_password')
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AlunoChangePasswordSerialser(instance=instance, data=request.data,
                                                     partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response({'result': 'Senha alterada'})


class MedicoesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsMedicoesPermissions]
    queryset = Medicao.objects.all()
    serializer_class = MedicoesSerializer
    filter_class = MedicaoFilter

    def get_queryset(self):
        return self.queryset.filter(aluno_id=self.kwargs['aluno_pk'])
