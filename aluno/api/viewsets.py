from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_api.api.viewsets import ModelViewSetOwner
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = AlunoSerializer(instance=instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        aluno = serializer.instance
        serializer = AlunoSerializer(instance=aluno)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_name='change_password', url_path='change_password')
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AlunoChangePasswordSerialser(instance=instance, data=request.data,
                                                     partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response({'result': 'Senha alterada'})