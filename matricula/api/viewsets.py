from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from ..models import Matricula, Mensalidade
from .serializers import MatriculaSerializerOutput, MensalidadeSerializerOutput


class MatriculaViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializerOutput


class MensalidadeViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Mensalidade.objects.all()
    serializer_class = MensalidadeSerializerOutput

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(matricula=self.kwargs['matricula_pk'])