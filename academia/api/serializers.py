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
    nome = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message='Este email já está sendo usado por outro usuário')])
    password = serializers.CharField(write_only=True)
    cnpj = serializers.CharField(required=False, write_only=True, validators=[UniqueValidator(queryset=Academia.objects.all(), message='Este cnpj já está sendo usado por outro usuário')])
    telefone = serializers.CharField(required=False, write_only=True)
    endereco = serializers.CharField(required=False, write_only=True)
    token = serializers.CharField(source='user.auth_token.key', read_only=True)
    user_id = serializers.CharField(source='user.pk', read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.pop('nome'),
                                        email=validated_data.pop('email'),
                                        password=validated_data.pop('password')
                                        )
        validated_data['user'] = user

        aluno = Academia.objects.create(**validated_data)

        return aluno


class AcademiaSerializerUpdateInput(AcademiaSerializerInput):
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs.pop('password') if attrs.get('password') else None

        if attrs.get('nome'):
            nome = attrs.pop('nome')
            attrs['username'] = nome

        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr in ('username', 'email'):
                setattr(instance.user, attr, value)
            else:
                setattr(instance, attr, value)

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