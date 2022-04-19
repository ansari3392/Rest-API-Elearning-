from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from account.models import Profile

User = get_user_model()


class TestUserCreationSignal(APITestCase):
    def setUp(self) -> None:
        pass

    def test_profile_creation_after_registration(self):
        user = User.objects.create_user(
            username='Eliiiii',
            password='1234789'
        )
        self.assertEqual(Profile.objects.count(user=user), 1)
        self.assertEqual(Profile.objects.first().user, user)
