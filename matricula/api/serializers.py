from rest_framework import serializers

from academia.api.serializers import AcademiaSerializer
from aluno.api.serializers import AlunoSerializer
from ..models import Matricula, Mensalidade
from ..constants import MEIOS_PAGAMENTO, RAZOES
from rest_framework.exceptions import ValidationError


class MatriculaSerializerOutput(serializers.ModelSerializer):
    aluno = AlunoSerializer()
    academia = AcademiaSerializer()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Matricula
        fields = ('id', 'aluno', 'academia', 'status', 'dt_matricula')


class MensalidadeSerializerOutput(serializers.ModelSerializer):
    matricula = MatriculaSerializerOutput()
    status = serializers.CharField(source='get_status_display')
    mes_referente = serializers.CharField(source='get_mes_referente_display')
    meio_pagamento = serializers.CharField(source='get_meio_pagamento_display')
    razao_nulo = serializers.CharField(source='get_razao_nulo_display')

    class Meta:
        model = Mensalidade
        fields = ('id', 'matricula', 'valor', 'mes_referente', 'dt_vencimento',
                  'status', 'razao_nulo', 'meio_pagamento',)


class MensalidadeSerializerCreate(serializers.ModelSerializer):
    valor = serializers.FloatField(write_only=True)
    qtd_parcelas = serializers.IntegerField(write_only=True)
    mes_referente = serializers.IntegerField(write_only=True)
    ano = serializers.IntegerField(write_only=True)
    mensalidades = serializers.SerializerMethodField()

    def get_mensalidades(self, objs):
        return MensalidadeSerializerOutput(objs, many=True).data

    def create(self, validated_data):
        matricula_pk = self.context.get('view').kwargs['matricula_pk']
        mensalidades = Mensalidade.objects.generate_mensalidades(matricula_pk, **validated_data)
        return mensalidades

    class Meta:
        model = Mensalidade
        fields = ('valor', 'mes_referente', 'ano', 'qtd_parcelas', 'mensalidades')


class MensalidadePagementoSerializer(serializers.ModelSerializer):
    meio_pagamento = serializers.CharField()
    criar_nova = serializers.BooleanField(default=False)

    def validate_meio_pagamento(self, meio):
        meios_validos = list(map(lambda meios: meios[0], MEIOS_PAGAMENTO))
        if meio not in meios_validos:
            raise ValidationError('Meio de pagamento inválido')
        return meio

    class Meta:
        model = Mensalidade
        fields = ('meio_pagamento', 'criar_nova')


class MensalidadeAnularSerializer(serializers.ModelSerializer):
    razao_nulo = serializers.CharField()
    criar_nova = serializers.BooleanField(default=False)

    def validate_razao_nulo(self, razao):
        razoes_validas = list(map(lambda meios: meios[0], RAZOES))
        if razao not in razoes_validas:
            raise ValidationError(f'Razão inválida, solicite as disponiveis: {razoes_validas}')
        return razao

    class Meta:
        model = Mensalidade
        fields = ('razao_nulo', 'criar_nova')