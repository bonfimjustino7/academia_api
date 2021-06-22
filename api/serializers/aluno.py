from rest_framework import serializers
from core.models import Aluno


class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Aluno
        fields = ('id', 'nome', 'cpf', 'email', 'telefone', 'endereco')
