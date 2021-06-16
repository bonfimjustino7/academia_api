from rest_framework import viewsets

from api.serializers.academia import AcademiaSerializer
from core.models import Academia


class AcademiaViewSet(viewsets.ModelViewSet):
    queryset = Academia.objects.all()
    serializer_class = AcademiaSerializer
