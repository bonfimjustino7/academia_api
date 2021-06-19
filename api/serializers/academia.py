from rest_framework import serializers
from core.models import Academia


class AcademiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academia
        fields = ('id', 'nome', 'cnpj', 'email', 'telefone', 'endereco')
