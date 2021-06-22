from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
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
                username = UserModel.objects.get(email=email).username
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)

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

