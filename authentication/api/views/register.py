from django.contrib.auth import get_user_model, login
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from authentication.otp_services import otp_service

from authentication.api.serializers.register import RegisterSerializer, UserOTPSerializer

User = get_user_model()


class LoginRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.is_verified:
            state = 'login'
        elif user and not user.is_verified:
            state = 'register'
        else:
            state = 'register'
            User.objects.create_user(phone_number=phone_number)

        if otp_service.has_otp(phone_number, state):
            data = {
                'statue': 400,
                'message': 'user has otp. please wait 2 seconds and try again'
            }
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            otp_num = otp_service.generate_otp()
            otp_service.send_otp_to_user(otp_num, phone_number, state)
            otp_service.save_otp(otp_num, phone_number, state)
            data = {
                'statue': 200,
                'message': 'OTP was sent. please verify OTP'
            }
            status_code = status.HTTP_200_OK
        return Response({'data': data}, status=status_code)


class ValidateOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserOTPSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        otp = serializer.validated_data.get('otp')
        user = get_object_or_404(User, phone_number=phone_number)
        if user.is_verified:
            state = 'login'
        else:
            state = 'register'
        if otp_service.validate_otp(otp, phone_number, state):
            if not user.is_verified:
                user.is_verified = True
                user.save()
            otp_service.remove_otp(phone_number, state)
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            status_code = status.HTTP_200_OK

            return Response(data, status=status_code)

        else:
            data = {
                'message': 'OTP is incorrect, please send correct OTP'
            }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(data, status=status_code)









