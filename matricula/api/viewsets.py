from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as RestValidationError


from ..filters import MensalidadeFilters, MatriculaFilters
from ..models import Matricula, Mensalidade
from .serializers import MatriculaSerializerOutput, MensalidadeSerializerOutput, \
    MensalidadeSerializerCreate, MensalidadePagementoSerializer, MensalidadeAnularSerializer


class MatriculaViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Matricula.objects.all().order_by('status', 'aluno__user__username')
    serializer_class = MatriculaSerializerOutput
    filter_class = MatriculaFilters

    # retorna a matricula do aluno autenticado ou as matriculas da academia
    def get_queryset(self):
        return self.queryset.filter(Q(aluno__user=self.request.user) | Q(academia__user=self.request.user))


class MensalidadeViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Mensalidade.objects.all()
    serializer_class = MensalidadeSerializerOutput
    filter_class = MensalidadeFilters

    def get_serializer_class(self):
        if self.action == 'create':
            return MensalidadeSerializerCreate
        return super(MensalidadeViewSet, self).get_serializer_class()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(Q(matricula__aluno__user=self.request.user) | Q(matricula__academia__user=self.request.user),
                                    matricula=self.kwargs['matricula_pk'])

    @action(detail=True, methods=['PATCH'], url_path='anular', serializer_class=MensalidadeAnularSerializer)
    def anular_mensalidade(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        razao = serializer.data['razao_nulo']
        criar_nova = serializer.data['criar_nova']

        mensalidade = self.get_object()
        try:
            mensalidade.anular(razao, criar_nova=criar_nova)
            mensalidade.save()
            return Response(MensalidadeSerializerOutput(mensalidade).data)
        except ValidationError as erro:
            raise RestValidationError({'mensalidade': list(erro)}, code=400)

    @action(detail=True, methods=['PATCH'], url_path='pagar', serializer_class=MensalidadePagementoSerializer)
    def pagar_mensalidade(self, request, *args, **kwargs):
        mensalidade = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        meio = serializer.data['meio_pagamento']
        criar_nova = serializer.data['criar_nova']
        try:
            mensalidade.pagar(meio, criar_nova=criar_nova)
            mensalidade.save()
        except ValidationError as error:
            raise RestValidationError({'mensalidade': list(error)}, code=400)

        return Response(MensalidadeSerializerOutput(mensalidade).data)



