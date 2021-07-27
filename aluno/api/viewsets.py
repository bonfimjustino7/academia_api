from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_api.api.viewsets import ModelViewSetOwner
from matricula.models import Matricula
from .serializers import AlunoSerializer, AlunoSerializerInput, AlunoSerializerUpdateInput, \
    AlunoChangePasswordSerialser
from ..models import Aluno


class AlunoViewSet(ModelViewSetOwner):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return AlunoSerializerUpdateInput
        elif self.action == 'create':
            return AlunoSerializerInput
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated()]
        return super(AlunoViewSet, self).get_permissions()

    def get_queryset(self):
        matricula = Matricula.objects.filter(Q(aluno__user=self.request.user) | Q(academia__user=self.request.user))
        if not matricula.exists():
            return self.queryset.none()
        return super(AlunoViewSet, self).get_queryset()

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