from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    def validate(self, attrs: dict) -> dict:
        email = attrs.get('email')
        phone = attrs.get('phone_number')
        if all([email, phone]):
            raise serializers.ValidationError('you cant send both email and phone number')
        if not any([email, phone]):
            raise serializers.ValidationError('you should send email or phone number')
        return attrs


class UserOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    otp = serializers.IntegerField(
        required=True,
        allow_null=False,
            )

    def validate(self, attrs: dict) -> dict:
        email = attrs.get('email')
        phone = attrs.get('phone_number')
        if all([email, phone]):
            raise serializers.ValidationError('kire khar')
        if not any([email, phone]):
            raise serializers.ValidationError('kire asb')
        return attrs





