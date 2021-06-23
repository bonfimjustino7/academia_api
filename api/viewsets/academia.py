from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from ..serializers.academia import AcademiaSerializer, AcademiaSerializerInput, AcademiaSerializerUpdateInput
from core.models import Academia
from rest_framework.response import Response


class AcademiaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Academia.objects.all()
    serializer_class = AcademiaSerializer

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