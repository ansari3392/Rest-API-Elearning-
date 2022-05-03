from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from django.utils.http import urlencode

User = get_user_model()

def create_user(phone_number, name):
    return User.objects.create(
       phone_number=phone_number,
       first_name=name,
       is_verified=True
    )

def create_admin(phone_number, name):
    return User.objects.create(
        phone_number=phone_number,
        first_name=name,
        is_staff=True,
        is_superuser=True,
        is_verified=True
    )


def reverse_querystring(url, query_kwargs=None):
    """ reverse('appname:api:name',  query_kwargs={'search': 'Bob'}) """
    base_url = reverse(url)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url
