from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from authentication.api.serializers.login import UsernamePasswordSerializer

User = get_user_model()


class PasswordLogin(APIView):
    serializer_class = UsernamePasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UsernamePasswordSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        password = serializer.validated_data.get('password')

        if email:
            user = authenticate(username=email, password=password)
            if user is not None and user.is_active:
                refresh = RefreshToken.for_user(user)
                data = {
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },
                    'status': status.HTTP_200_OK
                }

            else:
                data = {
                    'status': status.HTTP_400_BAD_REQUEST
                }
            return Response(data)

        else:
            user = authenticate(username=phone_number, password=password)
            if user is not None and user.is_active:
                refresh = RefreshToken.for_user(user)
                data = {
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },
                    'status': status.HTTP_200_OK
                }

            else:
                data = {
                    'status': HTTP_400_BAD_REQUEST
                }
            return Response(data)
