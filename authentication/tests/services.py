from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(phone_number):
    return User.objects.create(
       phone_number=phone_number,
       is_verified=True
    )

def create_admin(phone_number):
    return User.objects.create(
        phone_number=phone_number,
        is_staff=True,
        is_superuser=True,
        is_verified=True
    )
