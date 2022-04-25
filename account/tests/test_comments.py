from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from Blog.models import Article
from account.tests.service import create_user, reverse_querystring
from comment.models import Comment

User = get_user_model()

class CommentViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = create_user('09224282991')
        self.user2 = create_user('09224282992')
        refresh2 = RefreshToken.for_user(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh2.access_token}')
        self.article1 = Article.objects.create(title='test', description='testtttt', author=self.user1, is_published=True)

    def test_create_comment(self):
        self.url = reverse('comment:api:create_comment')
        data = {
            'description': 'big_like',
            'article': self.article1.sku,
            'is_private': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.description, 'big_like')
        self.assertEqual(comment.article.sku, self.article1.sku)
        self.assertTrue(comment.is_private)
        self.assertFalse(comment.is_active)

    def test_can_create_comment_unauthenticated(self):
        self.client.logout()
        self.url = reverse('comment:api:create_comment')
        data = {
            'description': 'big_like',
            'article': self.article1.sku,
            'is_private': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_active_comment_fail(self):
        url = reverse('comment:api:create_comment')
        data = {
            'description': 'big_like',
            'article': self.article1.sku,
            'is_private': True,
            'is_active': True
        }
        self.client.post(url, data)
        comment = Comment.objects.first()
        self.assertFalse(comment.is_active)

    def test_can_get_my_comment_list(self):
        Comment.objects.create(article=self.article1, description='like', author=self.user2)
        url = reverse('account:api:my_comments')
        response = self.client.get(url)
        comment_count = Comment.objects.filter(author=self.user2).count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), comment_count)
        comment = response.data.get('results')[0]
        self.assertIn('sku', comment)

    def test_can_update_comment(self):
        Comment.objects.create(article=self.article1, description='like', author=self.user2)
        comment= Comment.objects.first()
        url = reverse('account:api:update_comment', kwargs={'pk': comment.id})
        data = {
            'description': "very good",
            'is_active': True,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('description'), 'very good')
        self.assertFalse(response.data.get('is_active'))

    def test_can_update_active_comment(self):
        Comment.objects.create(article=self.article1, description='like', author=self.user2, is_active=True)
        comment= Comment.objects.first()
        url = reverse('account:api:update_comment', kwargs={'pk': comment.id})
        data = {
            'description': "very good"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_delete_comment(self):
        Comment.objects.create(article=self.article1, description='like', author=self.user2,)
        comment = Comment.objects.first()
        url = reverse('account:api:delete_comment', kwargs={'pk': comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_get_all_active_comment(self):
        Comment.objects.create(article=self.article1, description='like', author=self.user2, is_active=True, is_private=False)
        url = reverse('comment:api:comment_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_can_get_all_active_comment_of_an_article(self):
        Comment.objects.create(article=self.article1, description='like', author=self.user2, is_active=True)
        url = reverse_querystring('comment:api:comment_list', query_kwargs={'article_sku': self.article1.sku})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

