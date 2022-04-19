from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from Blog.models import Article
from Blog.tests.service import create_user, create_admin

User = get_user_model()

class ArticleTest(APITestCase):
    def setUp(self):
        self.user = create_admin('mahtab', 'mahtab@gmail.com')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_article_by_admin(self):
        url = reverse('blog:api:article-list')
        data = {
            'title': 'testing',
            'description': 'testttt',
            'is_published': True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'testing')

    def test_update_article_by_admin(self):
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        data = {
            'title': 'testing',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'testing')

    def test_get_articles_list(self):
        self.client.logout()
        Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        article_count = Article.objects.all().count()
        self.assertEqual(response.data.get('count'), article_count)

    def test_get_articles_detail(self):
        self.client.logout()
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-detail', kwargs={'pk':article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_article_by_author(self):
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)








