from rest_framework import serializers
from api.serializers.academia import AcademiaSerializer
from core.models import TokenAcademia


class AuthAcademiaSerializer(serializers.Serializer):
    academia = AcademiaSerializer(source='user')
    token = serializers.CharField(source='key')

    class Meta:
        model = TokenAcademia
        fields = ('token', 'academia',)


class AuthAcademiaValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField()
