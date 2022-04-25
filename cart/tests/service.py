from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from course.models import Course

User = get_user_model()


def create_user(phone_number):
    return User.objects.create(
       phone_number=phone_number,
       is_verified=True
    )







