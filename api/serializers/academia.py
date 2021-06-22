from rest_framework import serializers
from core.models import Academia


class AcademiaSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Academia
        fields = ('id', 'nome', 'email', 'cnpj', 'telefone', 'endereco')
