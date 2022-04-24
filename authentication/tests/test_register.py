from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from authentication.otp_services import otp_service
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            phone_number='09224282991',
            is_verified=True
        )
        self.user.save()

    def tearDown(self) -> None:
        cache.clear()

    def test_refresh_token_success(self):
        refresh = RefreshToken.for_user(self.user)
        data = {
            'refresh': str(refresh)
        }
        url = reverse('token_refresh')
        response = self.client.post(url, data)
        self.assertIn('access', response.data)
        with self.assertNumQueries(0):
            self.client.post(url, data)

    def test_user_register_send_otp_success(self):
        self.url = reverse('authentication:api:login')
        data = {
            "phone_number": "09224282992",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.filter(phone_number='09224282992')
        self.assertTrue(user.exists())
        self.assertFalse(user.first().is_verified)
        with self.assertNumQueries(1):
            self.client.post(self.url, data)

    def test_user_register_has_otp_fail(self):
        self.url = reverse('authentication:api:login')
        otp = otp_service.generate_otp()
        otp_service.save_otp(otp, '09224282992', 'register')
        data = {
            "phone_number": "09224282992",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.assertNumQueries(1):
            self.client.post(self.url, data)

    def test_user_register_enter_otp_success(self):
        User.objects.create_user(
            phone_number='09224282993',
            is_verified=False
        )
        self.user.save()

        self.url = reverse('authentication:api:verify_login')
        otp = otp_service.generate_otp()
        otp_service.save_otp(otp, '09224282993', 'register')
        data = {
            'phone_number': '09224282993',
            'otp': otp
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        user = User.objects.filter(phone_number='09224282993')
        self.assertTrue(user.first().is_verified)
        with self.assertNumQueries(1):
            self.client.post(self.url, data)

    def test_user_register_enter_wrong_otp_fail(self):
        User.objects.create_user(
            phone_number='09224282993',
            is_verified=False
        )
        self.user.save()

        url = reverse('authentication:api:verify_login')
        otp = otp_service.generate_otp()
        otp_service.save_otp(otp, '09224282993', 'register')
        data = {
            'phone_number': '09224282993',
            'otp': 2222
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_unauthorized_user_enter_otp_fail(self):
        url = reverse('authentication:api:verify_login')
        otp = otp_service.generate_otp()
        otp_service.save_otp(otp, '09224282993', 'register')
        data = {
            'phone_number': '09224282993',
            'otp': otp
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

    def test_cache_remove_otp_after_register_success(self):
        User.objects.create_user(
            phone_number='09224282994',
            is_verified=False
        )
        self.user.save()
        otp = otp_service.generate_otp()
        otp_before_login = otp_service.save_otp(otp, '09224282994', 'register')

        url = reverse('authentication:api:verify_login')
        data = {
            'phone_number': '09224282994',
            'otp': otp
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        otp_after_login = cache.get(otp_before_login)
        self.assertIsNone(otp_after_login)

    def test_user_login_send_otp_success(self):
        self.url = reverse('authentication:api:login')
        data = {
            "phone_number": "09224282991"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_has_otp_fail(self):
        self.url = reverse('authentication:api:login')
        otp = otp_service.generate_otp()
        otp_service.save_otp(otp, '09224282991', 'login')
        data = {
            "phone_number": "09224282991",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_enter_otp_success(self):
        url = reverse('authentication:api:verify_login')
        otp = otp_service.generate_otp()
        otp_service.save_otp(otp, '09224282991', 'login')
        data = {
            'phone_number': '09224282991',
            'otp': otp
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_cache_remove_otp_after_login_success(self):
        otp = otp_service.generate_otp()
        otp_before_login = otp_service.save_otp(otp, '09224282991', 'login')

        url = reverse('authentication:api:verify_login')
        data = {
            'phone_number': '09224282991',
            'otp': otp
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        otp_after_login = cache.get(otp_before_login)
        self.assertIsNone(otp_after_login)


















