from rest_framework import serializers

from academia.api.serializers import AcademiaSerializer
from aluno.api.serializers import AlunoSerializer
from ..models import Matricula, Mensalidade


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

    class Meta:
        model = Mensalidade
        fields = ('id', 'matricula', 'mes_referente', 'dt_vencimento', 'status')