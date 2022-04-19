import random

from redis import Redis
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()
r = Redis(host=settings.OTP_REDIS_HOST,
          port=settings.OTP_REDIS_PORT,
          db=settings.OTP_REDIS_NAME)

class OTPService:

    def __init__(self):
        self.r = r

    def has_otp(self, phone_number):
        return True if self.r.exists(phone_number) else False

    @staticmethod
    def generate_otp():
        otp = random.randint(1000, 9999)
        return otp

    def save_otp(self, otp, phone_number):
        self.r.setex(phone_number, settings.OTP_EXPIRY_SECONDS, otp)

    @staticmethod
    def send_otp_to_user(otp, phone_number):
        pass

    def validate_otp(self, otp, phone_number):
        try:
            otp = int(otp)
        except:
            return False
        if otp:
            otp_in_redis = self.r.get(phone_number)
            if otp_in_redis and otp_in_redis == otp:
                return True
        return False

    def remove_phone(self, phone_number):
        self.r.delete(phone_number)






