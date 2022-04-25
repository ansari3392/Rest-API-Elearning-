from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from Blog.models import Article
from Blog.tests.service import create_user, create_admin
from cms.models import Tag

User = get_user_model()

class ArticleTest(APITestCase):
    def setUp(self):
        self.user = create_admin('09224282991')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.tag1 = Tag.objects.create(name="coding")
        self.tag2 = Tag.objects.create(name="learning")

    def test_create_article_by_admin_without_tags(self):
        url = reverse('blog:api:article-list')
        data = {
            'title': 'testing',
            'description': 'testttt',
            'is_published': True,

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'testing')
        with self.assertNumQueries(4):
            self.client.post(url, data)

    def test_create_article_by_admin_with_tags(self):
        url = reverse('blog:api:article-list')
        data = {
            'title': 'testing',
            'description': 'testttt',
            'is_published': True,
            'tag_list': ['sport']

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'testing')
        self.assertEqual(len(response.data.get("tags")), 1)
        with self.assertNumQueries(6):
            self.client.post(url, data)

    def test_update_article_by_admin_without_tags(self):
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        data = {
            'title': 'testing',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'testing')

    def test_update_article_by_admin_tags(self):
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        article.tags.set([self.tag2, self.tag1])

        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        data = {
            'title': 'testing',
            'tag_list': []
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'testing')
        self.assertEqual(len(response.data.get("tags")), 0)

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
        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_article_by_author(self):
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)








