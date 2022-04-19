from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from course.models import Course

User = get_user_model()

def create_user(username, email):
    return User.objects.create(
        username=username,
        email=email,
        password='somepassword'
    )







