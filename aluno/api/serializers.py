from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from academia.models import Academia
from matricula.constants import ATIVA
from ..models import Aluno
from matricula.models import Matricula

User = get_user_model()


class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    academia = serializers.SerializerMethodField()

    def get_academia(self, obj):
        queryset = Matricula.objects.filter(aluno=obj)
        if queryset.exists():
            academia = queryset.last().academia.pk
            return academia
        return None

    class Meta:
        model = Aluno
        fields = ('id', 'nome', 'cpf', 'email', 'telefone', 'endereco', 'academia')


class AlunoSerializerInput(serializers.Serializer):
    nome = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, validators=[
        UniqueValidator(queryset=User.objects.all(),
                        message='Este email já está sendo usado por outro usuário')])
    cpf = serializers.CharField(required=False, write_only=True, validators=[
        UniqueValidator(queryset=Aluno.objects.all(),
                        message='Este cpf já está sendo usado por outro usuário')])
    telefone = serializers.CharField(required=False, write_only=True)
    endereco = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(write_only=True)
    academia = serializers.PrimaryKeyRelatedField(queryset=Academia.objects.all(), write_only=True)

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')):
            raise serializers.ValidationError({"email": "Este email já está sendo usado por outro usuário"})

        return attrs

    def create(self, validated_data):
        aluno = Aluno.objects.create_user(**validated_data)
        return aluno


class AlunoSerializerUpdateInput(AlunoSerializerInput):
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        if self.instance and self.instance.user.email != attrs.get('email'):
            return super(AlunoSerializerUpdateInput, self).validate(attrs)

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
            elif attr in ('academia',) and value:
                matricula = Matricula.objects.filter(aluno=instance, status=ATIVA).last()
                matricula.academia = value
                matricula.save()
            else:
                setattr(instance, attr, value)
        instance.user.save()
        instance.save()

        return instance


class AlunoChangePasswordSerialser(serializers.Serializer):
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
