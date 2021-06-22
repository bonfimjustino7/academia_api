from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers.academia import AcademiaSerializer
from core.models import Academia


class AcademiaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Academia.objects.all()
    serializer_class = AcademiaSerializer
