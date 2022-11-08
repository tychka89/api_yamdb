from rest_framework import permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .serializers import (UserSerializer, TokenSerializer,
                          RegisterDataSerializer)


class RegistrationViewSet(viewsets.ModelViewset):
    serializer = RegisterDataSerializer
    permission_classes = permissions.AllowAny


class GetTokenViewSet(viewsets.ModelViewSet):
    serializer = TokenSerializer
    permission_classes = permissions.AllowAny
