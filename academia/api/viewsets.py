from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .serializers import AcademiaSerializer, AcademiaSerializerInput, \
    AcademiaSerializerUpdateInput, AcademiaChangePasswordSerialser
from ..models import Academia
from rest_framework.response import Response

User = get_user_model()


class AcademiaViewSet(viewsets.ModelViewSet):
    queryset = Academia.objects.all()
    serializer_class = AcademiaSerializer

    def get_permissions(self):
        if self.action != 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return AcademiaSerializerUpdateInput
        elif self.action == 'create':
            return AcademiaSerializerInput
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = AcademiaSerializer(instance=instance)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_name='change_password', url_path='change_password')
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AcademiaChangePasswordSerialser(instance=instance, data=request.data,
                                                     partial=True)
        serializer.is_valid(raise_exception=True)
        if request.auth.user != instance.user:
            raise ValidationError(detail={'error': 'Token não autorizado'}, code=status.HTTP_401_UNAUTHORIZED)

        self.perform_update(serializer)

        return Response({'result': 'Senha alterada'})
