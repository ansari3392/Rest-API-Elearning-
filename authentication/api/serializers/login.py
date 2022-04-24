from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, allow_blank=True)
    email = serializers.CharField(write_only=True, allow_blank=True)

    def validate(self, attrs):
        if attrs['phone_number'] and attrs['email']:
            raise serializers.ValidationError({"error": "you only can send email or phone number"})
        elif not attrs['phone_number'] and not attrs['email']:
            raise serializers.ValidationError({"error": "you must send email or phone number"})
        return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


class UsernamePasswordSerializer(LoginSerializer, PasswordSerializer):
    pass


