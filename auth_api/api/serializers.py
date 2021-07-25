from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class AuthSerializerInput(serializers.Serializer):
    email = serializers.EmailField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Senha",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label="Token",
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                UserModel = get_user_model()
                user = authenticate(request=self.context.get('request'),
                                    email=email, password=password)

            except UserModel.DoesNotExist:
                msg = 'Não existe nenhum usuário com este email.'
                raise serializers.ValidationError(msg, code='authorization')

            if not user:
                msg = 'Senha inválida.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Você deve passar o email e senha corretos.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class AuthSerializerOutput(serializers.Serializer):
    token = serializers.CharField(read_only=True, source='auth_token.key')
    user_id = serializers.SerializerMethodField()
    nome = serializers.CharField(read_only=True, source='username')
    is_aluno = serializers.SerializerMethodField()
    is_academia = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        if hasattr(obj, 'aluno'):
            return obj.aluno.pk
        else:
            return obj.academia.pk

    def get_is_aluno(self, obj):
        return hasattr(obj, 'aluno')

    def get_is_academia(self, obj):
        return hasattr(obj, 'academia')
