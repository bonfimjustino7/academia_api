from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from core.models import Academia, TokenAcademia

from api.serializers.auth import AuthAcademiaSerializer, AuthAcademiaValidateSerializer


class AuthToken(GenericViewSet):
    queryset = Academia.objects.all()

    def authenticate(self, serializer, model):
        academia_instance = get_object_or_404(model,
                                              email=serializer.validated_data.get('email'))
        if not check_password(serializer.validated_data.get('senha'), academia_instance.senha):
            raise ValidationError({
                'detail': 'Senha incorreta'
            })
        return academia_instance

    def get_serializer_class(self):
        if self.action == 'academia':
            return AuthAcademiaValidateSerializer

    @action(detail=False, methods=['post'], url_path='academia', url_name='auth_academia')
    def academia(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        academia_instance = self.authenticate(serializer, Academia)
        token_academia = TokenAcademia.objects.get(user=academia_instance)
        serialiser_output = AuthAcademiaSerializer(instance=token_academia)

        return Response(serialiser_output.data)

