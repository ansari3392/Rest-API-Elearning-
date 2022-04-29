# test comments for admin side
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from comment.tests.service import create_admin


class CommentTest(APITestCase):
    def setUp(self) -> None:
        self.user = create_admin('09224282991')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')


