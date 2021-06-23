from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Aluno
from rest_framework.exceptions import ValidationError


class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Aluno
        fields = ('id', 'nome', 'cpf', 'email', 'telefone', 'endereco')


class AlunoSerializerInput(serializers.Serializer):
    nome = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    cnpj = serializers.CharField(required=False, write_only=True)
    telefone = serializers.CharField(required=False, write_only=True)
    endereco = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(write_only=True)

    def is_valid(self, raise_exception=False):
        super(AlunoSerializerInput, self).is_valid(raise_exception)
        User = get_user_model()
        if User.objects.filter(email=self.validated_data.get('email')).exists():
            raise ValidationError({'email': 'Este email já está sendo usado por outro usuário'})

        return True

    def create(self, validated_data):
        User = get_user_model()

        user = User.objects.create_user(username=validated_data.pop('nome'),
                                        email=validated_data.pop('email'),
                                        password=validated_data.pop('password')
                                        )
        validated_data['user'] = user

        aluno = Aluno.objects.create(**validated_data)

        return aluno