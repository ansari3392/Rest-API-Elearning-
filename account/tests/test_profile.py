import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class UserViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('account:api:my_profile')
        self.user = User.objects.create(username='mahtab', password='verystrongpassword')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # self.token = Token.objects.create(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_profile_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_authenticated(self):
        data = {
                "first_name": "fati",
                "last_name": "ansari",
                "email": "mehri@gmail.com",
                "username": "fatimaaaaaaa",
                "profile": {
                    "phone_number": "09224282991",
                    "gender": "female",
                    "bio": "I am a programmer",
                    "is_teacher": False,
                    "is_consultant": True
                }
            }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), 'fati', )
        self.assertEqual(response.data.get('last_name'), 'ansari', )
        self.assertEqual(response.data.get('email'), 'mehri@gmail.com', )
        self.assertEqual(response.data.get('username'), 'fatimaaaaaaa', )
        self.assertEqual(response.data.get('profile').get('phone_number'), '09224282991', )
        self.assertEqual(response.data.get('profile').get('gender'), 'female', )
