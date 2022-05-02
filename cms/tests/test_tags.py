from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from cms.models import Tag
from cms.tests.service import create_user, create_admin


class TagTest(APITestCase):
    def setUp(self) -> None:
        self.user = create_admin('09224282991')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_tag_by_admin_success(self):
        url = reverse('cms:api:tag-list')
        data = {
            'name': 'testing',

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'testing')
        with self.assertNumQueries(2):
            self.client.post(url, data)

    def test_create_tag_by_non_admin_fail(self):
        self.client.logout()
        self.user = create_user('09224282992')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('cms:api:tag-list')
        data = {
            'name': 'testing',

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.assertNumQueries(1):
            self.client.post(url, data)

    def test_update_tag_by_admin_success(self):
        tag = Tag.objects.create(name='testss')
        url = reverse('cms:api:tag-detail', kwargs={'pk': tag.pk})
        data = {
            'name': 'testing',

        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertNumQueries(1):
            self.client.post(url, data)

    def test_update_tag_by_non_admin_fail(self):
        tag = Tag.objects.create(name='testss')
        self.client.logout()
        self.user = create_user('09224282992')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('cms:api:tag-detail', kwargs={'pk': tag.pk})
        data = {
            'name': 'testing',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.assertNumQueries(1):
            self.client.post(url, data)

    def test_delete_tag_by_admin_success(self):
        tag = Tag.objects.create(name='test')
        url = reverse('cms:api:tag-detail', kwargs={'pk': tag.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_tag_by_non_admin_fail(self):
        tag = Tag.objects.create(name='test')
        self.client.logout()
        self.user = create_user('09224282992')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('cms:api:tag-detail', kwargs={'pk': tag.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tags_list(self):
        self.client.logout()
        tag_list = ['test1', 'test2', 'test3', 'test4']
        for tag in tag_list:
            tag, _ = Tag.objects.get_or_create(name=tag)

        url = reverse('cms:api:tag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tags_count = Tag.objects.all().count()
        self.assertEqual(response.data.get('count'), tags_count)
        tag0 = response.data.get('results')[0]
        self.assertEqual(tag0.get('name'), 'test1')

    def test_get_tag_detail(self):
        self.client.logout()
        tag = Tag.objects.create(name='test3')
        url = reverse('cms:api:tag-detail', kwargs={'pk': tag.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), 'test3')
