from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse


User = get_user_model()

def create_user(username, email):
    return User.objects.create(
        username=username,
        email=email,
        password='somepassword'
    )

def create_admin(username, email):
    return User.objects.create(
        username=username,
        email=email,
        password='somepassword',
        is_staff=True,
        is_superuser=True
    )


