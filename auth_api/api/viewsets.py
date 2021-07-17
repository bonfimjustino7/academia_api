from rest_framework import viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import AuthSerializer
from .permissions import IsAuthenticatedOwner


class AuthToken(ObtainAuthToken):
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ModelViewSetOwner(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    """
        ViewSet para models relacionados com usuario
    """
    def get_permissions(self):
        if self.action != 'create':
            permissions = [IsAuthenticatedOwner]
        else:
            permissions = []
        return [permission() for permission in permissions]