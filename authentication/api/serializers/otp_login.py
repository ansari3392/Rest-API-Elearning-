from rest_framework import serializers

class OTPLoginSerializer(serializers):
    phone_number = serializers.CharField(write_only=True,  unique=True,)
    email = serializers.CharField(write_only=True, unique=True,)

    def validate(self, attrs):
        if attrs['phone_number'] and attrs[' email']:
            raise serializers.ValidationError({"error": "you only can send email or phone number"})
        elif not attrs['phone_number'] and attrs[' email']:
            raise serializers.ValidationError({"error": "you must send email or phone number"})
        return attrs


