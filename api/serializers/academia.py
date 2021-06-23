from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Academia
from rest_framework.exceptions import ValidationError

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
    cnpj = serializers.CharField(required=False, write_only=True)
    telefone = serializers.CharField(required=False, write_only=True)
    endereco = serializers.CharField(required=False, write_only=True)

    def is_valid(self, raise_exception=False):
        super(AcademiaSerializerInput, self).is_valid(raise_exception)
        User = get_user_model()
        if User.objects.filter(email=self.validated_data.get('email')).exists():
            raise ValidationError({'email': 'Este email já está sendo usado por outro usuário'})

        return True

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.pop('nome'),
                                        email=validated_data.pop('email'),
                                        password=validated_data.pop('password')
                                        )
        validated_data['user'] = user

        aluno = Academia.objects.create(**validated_data)

        return aluno


class AcademiaSerializerUpdateInput(AcademiaSerializerInput):

    def is_valid(self, raise_exception=False):
        super(AcademiaSerializerInput, self).is_valid(raise_exception)
        if self.validated_data.get('email') != self.instance.user.email:
            if User.objects.filter(email=self.validated_data.get('email')).exists():
                raise ValidationError({'email': 'Este email já está sendo usado por outro usuário'})
        return True

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

        instance.save()
        return instance
