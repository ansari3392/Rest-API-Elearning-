from django.contrib.auth import get_user_model
from django.utils.http import urlencode
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

    )

def reverse_querystring(url, query_kwargs=None):
    """ reverse('appname:api:name',  query_kwargs={'search': 'Bob'}) """
    base_url = reverse(url)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


