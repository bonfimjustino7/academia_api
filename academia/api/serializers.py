from django.contrib.auth import get_user_model
from rest_framework import serializers

from matricula.models import Matricula
from ..models import Academia
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class AcademiaSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Academia
        fields = ('id', 'nome', 'email', 'cnpj', 'telefone', 'endereco')


class AcademiaSerializerInput(serializers.Serializer):
    nome = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    cnpj = serializers.CharField(required=False, write_only=True,
                                 validators=[UniqueValidator(queryset=Academia.objects.all(),
                                                             message='Este cnpj já está sendo usado por outro usuário')])
    telefone = serializers.CharField(required=False, write_only=True)
    endereco = serializers.CharField(required=False, write_only=True)
    token = serializers.CharField(source='user.auth_token.key', read_only=True)
    user_id = serializers.CharField(source='user.pk', read_only=True)

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')):
            raise serializers.ValidationError({"email": "Este email já está sendo usado por outro usuário"})

        return attrs

    def create(self, validated_data):
        academia = Academia.objects.create_user(**validated_data)
        return academia


class AcademiaSerializerUpdateInput(AcademiaSerializerInput):
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        if self.instance and self.instance.user.email != attrs.get('email'):
            return super(AcademiaSerializerUpdateInput, self).validate(attrs)

        attrs.pop('password') if attrs.get('password') else None

        if attrs.get('nome'):
            nome = attrs.pop('nome')
            attrs['username'] = nome

        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'email':
                setattr(instance.user, attr, value)
            elif attr == 'nome':
                setattr(instance.user, 'username', value)
            else:
                setattr(instance, attr, value)
        instance.user.save()
        instance.save()

        return instance


class AcademiaChangePasswordSerialser(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    confirmed_password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        confirmed_password = attrs.pop('confirmed_password')
        if attrs.get('password') != confirmed_password:
            raise ValidationError({'password': ['Senha não combina com a confirmação']})
        return attrs

    def update(self, instance, validated_data):
        instance.user.set_password(validated_data.get('password'))
        instance.user.save()
        return instance