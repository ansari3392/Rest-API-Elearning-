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

    def test_create_article_by_admin_without_tags_success(self):
        url = reverse('blog:api:article-list')
        data = {
            'title': 'testing',
            'description': 'testttt',
            'is_published': True,

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'testing')
        self.assertEqual(response.data.get('description'), 'testttt')
        self.assertTrue(response.data.get('is_published'))
        with self.assertNumQueries(4):
            self.client.post(url, data)

    def test_create_article_by_admin_with_tags_success(self):
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

    def test_create_article_by_user_fail(self):
        self.client.logout()
        self.user = create_user('09224282996')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('blog:api:article-list')
        data = {
            'title': 'testing',
            'description': 'test',
            'is_published': True,

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_article_by_admin_without_tags(self):
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        data = {
            'title': 'testing',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'testing')
        self.assertEqual(response.data.get('description'), article.description)
        self.assertEqual(response.data.get('is_published'), article.is_published)
        self.assertEqual(response.data.get('author'), article.author.first_name)
        self.assertEqual(response.data.get('id'), article.id)

    def test_update_article_by_admin_with_tags_success(self):
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
        self.assertEqual(response.data.get('description'), article.description)
        self.assertEqual(response.data.get('is_published'), article.is_published)
        self.assertEqual(response.data.get('author'), article.author.first_name)
        self.assertEqual(response.data.get('id'), article.id)

    def test_update_article_by_user_fail(self):
        self.client.logout()
        self.user = create_user('09224282996')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        article.tags.set([self.tag2, self.tag1])

        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        data = {
            'title': 'testing',
            'tag_list': []
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_articles_list_success(self):
        self.client.logout()
        Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        article_count = Article.objects.all().count()
        self.assertEqual(response.data.get('count'), article_count)
        article = response.data.get('results')[0]
        self.assertEqual(article.get('title'), 'test')
        self.assertTrue(article.get('is_published'), True)

    def test_get_articles_detail_success(self):
        self.client.logout()
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), article.title)
        self.assertEqual(response.data.get('description'), article.description)
        self.assertEqual(response.data.get('is_published'), article.is_published)
        self.assertEqual(response.data.get('id'), article.id)
        self.assertEqual(response.data.get('author'), article.author.first_name)

    def test_delete_article_by_author_success(self):
        article = Article.objects.create(title='test', description='test again', is_published=True, author=self.user)
        url = reverse('blog:api:article-detail', kwargs={'pk': article.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)








