from rest_framework import viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializers import AuthSerializerInput, AuthSerializerOutput
from .permissions import IsAuthenticatedOwner


class AuthToken(ObtainAuthToken):
    serializer_class = AuthSerializerInput

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer_output = AuthSerializerOutput(instance=user)

        return Response(serializer_output.data)


class ModelViewSetOwner(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    """
        ViewSet para models relacionados com usuario
    """
    def get_permissions(self):
        if self.action == 'create':
            permissions = self.permission_classes
        else:
            permissions = [IsAuthenticatedOwner]
        return [permission() for permission in permissions]