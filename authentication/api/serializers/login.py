from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginSerializer(serializers):
    phone_number = serializers.CharField(write_only=True,  unique=True,)
    email = serializers.CharField(write_only=True, unique=True,)

    def validate(self, attrs):
        if attrs['phone_number'] and attrs[' email']:
            raise serializers.ValidationError({"error": "you only can send email or phone number"})
        elif not attrs['phone_number'] and attrs[' email']:
            raise serializers.ValidationError({"error": "you must send email or phone number"})
        return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_lenght=50, required=True)

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


class UsernamePasswordSerializer(LoginSerializer, PasswordSerializer):
    pass


