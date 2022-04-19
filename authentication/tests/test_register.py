from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class RegisterTestCase(APITestCase):

    def test_user_registration_ok(self):
        self.url = reverse('authentication:api:registration')
        data = {
            "username": "fati",
            "email": "ansari@gmail.com",
            "password": "6170025018a",
            "password2": "6170025018a"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("username"), "fati")
        self.assertEqual(response.data.get("email"), "ansari@gmail.com")

    def test_user_registration_same_username(self):
        self.user1 = User.objects.create_user(
            username='fati',
            email='ansari3392@gmail.com',
            password='123456aaaa',
        )
        self.url = reverse('authentication:api:registration')
        data = {
            "username": "fati",
            "email": "ansari@gmail.com",
            "password": "6170025018a",
            "password2": "6170025018a"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_same_email(self):
        self.user1 = User.objects.create_user(
            username='fatima',
            email='ansari2@gmail.com',
            password='123456aaaa',
        )
        self.url = reverse('authentication:api:registration')
        data = {
            "username": "fati",
            "email": "ansari2@gmail.com",
            "password": "6170025018a",
            "password2": "6170025018a"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_unequal_pass(self):
        self.url = reverse('authentication:api:registration')
        data = {
            "username": "fati",
            "email": "ansari1234@gmail.com",
            "password": "6170025018",
            "password2": "6170025018a"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)








