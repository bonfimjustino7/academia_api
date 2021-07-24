from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from ..filters import MensalidadeFilters
from ..models import Matricula, Mensalidade
from .serializers import MatriculaSerializerOutput, MensalidadeSerializerOutput


class MatriculaViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializerOutput

    def get_queryset(self):
        return self.queryset.filter(Q(aluno__user=self.request.user) | Q(academia__user=self.request.user))


class MensalidadeViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Mensalidade.objects.all()
    serializer_class = MensalidadeSerializerOutput
    filter_class = MensalidadeFilters

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(Q(matricula__aluno__user=self.request.user) | Q(matricula__academia__user=self.request.user),
                                    matricula=self.kwargs['matricula_pk'])