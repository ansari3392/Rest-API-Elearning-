from django.contrib.auth import get_user_model
from django.utils.http import urlencode
from rest_framework.reverse import reverse

User = get_user_model()

def create_user(phone_number, name):
    return User.objects.create(
       phone_number=phone_number,
       is_verified=True,
       first_name=name
    )

def reverse_querystring(url, query_kwargs=None):
    """ reverse('appname:api:name',  query_kwargs={'search': 'Bob'}) """
    base_url = reverse(url)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url
