from django.contrib.auth import get_user_model
from rest_framework import serializers

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
    nome = serializers.CharField(source='user.username')
    email = serializers.EmailField(write_only=True, validators=[
        UniqueValidator(queryset=User.objects.all(),
                        message='Este email já está sendo usado por outro usuário')])
    password = serializers.CharField(write_only=True)
    cnpj = serializers.CharField(required=False, write_only=True, allow_blank=True, allow_null=True,
                                 validators=[UniqueValidator(queryset=Academia.objects.all(),
                                                             message='Este cnpj já está sendo usado por outro usuário')])
    telefone = serializers.CharField(required=False, write_only=True, allow_blank=True, allow_null=True)
    endereco = serializers.CharField(required=False, write_only=True, allow_blank=True, allow_null=True)
    token = serializers.CharField(source='user.auth_token.key', read_only=True)
    user_id = serializers.CharField(source='pk', read_only=True)

    def to_internal_value(self, data):
        data = super(AcademiaSerializerInput, self).to_internal_value(data)
        data_output = data.copy()
        if data.get('user'):
            data_output['nome'] = data['user']['username']
            data_output.pop('user')

        return data_output

    def create(self, validated_data):
        academia = Academia.objects.create_user(**validated_data)
        return academia


class AcademiaSerializerUpdateInput(AcademiaSerializerInput):
    password = serializers.CharField(required=False)
    nome = serializers.CharField(required=False)
    email = serializers.EmailField(write_only=True, required=False)

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
            elif attr == 'username':
                setattr(instance.user, 'username', value)
            else:
                setattr(instance, attr, value)
        instance.user.save()
        instance.save()

        return instance


# TODO mover para o app auth
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