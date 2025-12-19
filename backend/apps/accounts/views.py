from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.accounts.serializers import RegisterSerializer
from apps.accounts.models import User


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.model(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({'group': 'users'})
            auth_keys = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data=auth_keys, status=status.HTTP_201_CREATED)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
