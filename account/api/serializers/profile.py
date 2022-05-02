from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from account.models.profile import Profile

User = get_user_model()

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'sku',
            'gender',
            'avatar',
            'bio',
            'is_teacher',
            'is_consultant'
        ]
        read_only_fields = (
            'avatar',  # for this field we should write new api, cause we cant send image with Postnman
        )


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )
