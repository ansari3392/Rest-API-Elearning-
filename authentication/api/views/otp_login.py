from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from authentication.api.serializers.login import LoginSerializer

User = get_user_model()


class SendOTPLoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        if email:
            user = User.objects.filter(email=email)
            if user.exists():
                # send_token_to_user with email
                pass
            else:
                raise Exception
        else:
            user = User.objects.filter(phone_number=phone_number)
            if user.exists():
                # send_token_to_user with phone number
                pass
            else:
                raise Exception


