from django.contrib.auth import get_user_model
from khayyam import JalaliDatetime
from pytz import timezone
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from account.models.profile import Profile

User = get_user_model()

class ProfileSerializer(ModelSerializer):
    created = SerializerMethodField()

    def get_created(self, obj):
        date = JalaliDatetime(
            obj.created.astimezone(tz=timezone('Asia/Tehran'))
        )
        return str(date)

    class Meta:
        model = Profile
        fields = [
            'id',
            'sku',
            'gender',
            'avatar',
            'bio',
            'is_teacher',
            'is_consultant',
            'created'
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
            'profile',
        )
