import random

from django.conf import settings
from django.contrib.auth import get_user_model
from redis import Redis
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache

User = get_user_model()
redis = Redis(
    host=settings.OTP_REDIS_HOST,
    port=settings.OTP_REDIS_PORT,
    db=settings.OTP_REDIS_NAME
)


class OTPService:

    def __init__(self):
        self.cache = cache

    @staticmethod
    def generate_cache_key(phone_number: str, state: str) -> str:
        return f"{phone_number}_{state}"

    def has_otp(self, phone_number: str, state: str) -> bool:
        cache_key = self.generate_cache_key(phone_number, state)
        return True if self.cache.get(cache_key) else False

    @staticmethod
    def generate_otp() -> int:
        otp = random.randint(1000, 9999)
        return otp

    def save_otp(self, otp: int, phone_number: str, state: str) -> None:
        cache_key = self.generate_cache_key(phone_number, state)
        self.cache.set(cache_key, otp, settings.OTP_EXPIRY_SECONDS)

    @staticmethod
    def send_otp_to_user(otp: int, phone_number: str, state: str) -> Response:
        # link = settings.OTP_SETTINGS['CLIENT'] + "module=TRANS_SMS&apikey=" + \
        #     settings.OTP_SETTINGS['API_KEY'] + "&to=" + phone_number + \
        #     "&from=" + settings.OTP_SETTINGS['SENDER_ID'] + \
        #     "&templatename=" + settings.OTP_SETTINGS['TEMPLATE_NAME'] + \
        #     "&var1=" + phone_number + "&var2=" + otp
        # print(link)
        # message = requests.get(link)
        print(otp)
        return Response({
                'statue': status.HTTP_200_OK,
                'details': 'OTP sent successfully.'
            })

    def validate_otp(self, otp: int, phone_number: str, state: str) -> bool:
        cache_key = self.generate_cache_key(phone_number, state)
        try:
            otp = int(otp)
        except ValueError:
            return False
        if otp:
            otp_in_cache = self.cache.get(cache_key)

            if otp_in_cache == otp:
                return True
        return False

    def remove_otp(self, phone_number: str, state: str) -> None:
        cache_key = self.generate_cache_key(phone_number, state)
        self.cache.delete(cache_key)


otp_service = OTPService()





