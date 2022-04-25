from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Profile
from categories.models import Category
from cms.models import Tag
from course.models import Course, CourseEpisode
from course.tests.service import create_user, create_admin, reverse_querystring
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class CourseEpisodeTest(APITestCase):

    def setUp(self):
        self.user = create_admin('09224282995')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.user2 = User.objects.create_user('09224282996')
        Profile.objects.filter(user=self.user2).update(is_teacher=True)
        self.cat1 = Category.objects.create(title="programming")
        self.tag1 = Tag.objects.create(name="coding")
        self.tag2 = Tag.objects.create(name="learning")
        self.course: Course = Course.objects.create(title="testing", description="testing again", teacher=self.user2,
                                                    category=self.cat1, )

    def test_create_course_episode_by_admin(self):
        url = reverse('course:api:course-episode-list')
        with open('course/tests/files/sample.mp4', 'rb') as f:
            file = SimpleUploadedFile('Name of the django file', f.read())
        data = {
            "course": self.course.sku,
            "number": 1,
            "title": "introduction",
            "duration": "02:05:01",
            "video": file

        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_episode_by_non_admin(self):
        self.client.logout()
        refresh = RefreshToken.for_user(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('course:api:course-episode-list')
        with open('course/tests/files/sample.mp4', 'rb') as f:
            file = SimpleUploadedFile('Name of the django file', f.read())
        data = {
            "course": self.course.sku,
            "number": 1,
            "title": "introduction",
            "duration": "02:05:01",
            "video": file

        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_episode_by_admin(self):
        with open('course/tests/files/sample.mp4', 'rb') as f:
            file = SimpleUploadedFile('Name of the django file', f.read())
        course_episode: CourseEpisode = CourseEpisode.objects.create(course=self.course, number=1,
                                                                     title="introduction", duration="02:05:01",
                                                                     video=file)
        url = reverse('course:api:course-episode-detail', kwargs={'pk': course_episode.pk})
        data = {
            "title": "introduction1"
        }
        response = self.client.patch(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), "introduction1")

    def test_update_course_episode_by_non_admin(self):
        self.client.logout()
        refresh = RefreshToken.for_user(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        with open('course/tests/files/sample.mp4', 'rb') as f:
            file = SimpleUploadedFile('Name of the django file', f.read())
        course_episode: CourseEpisode = CourseEpisode.objects.create(course=self.course, number=1,
                                                                     title="introduction", duration="02:05:01",
                                                                     video=file)
        url = reverse('course:api:course-episode-detail', kwargs={'pk': course_episode.pk})
        data = {
            "title": "introduction1"
        }
        response = self.client.patch(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_course_episode_by_admin(self):
        with open('course/tests/files/sample.mp4', 'rb') as f:
            file = SimpleUploadedFile('Name of the django file', f.read())
        course_episode: CourseEpisode = CourseEpisode.objects.create(course=self.course, number=1,
                                                                     title="introduction", duration="02:05:01",
                                                                     video=file)
        url = reverse('course:api:course-episode-detail', kwargs={'pk': course_episode.pk})
        response = self.client.delete(url, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_course_episode_by_non_admin(self):
        self.client.logout()
        refresh = RefreshToken.for_user(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        with open('course/tests/files/sample.mp4', 'rb') as f:
            file = SimpleUploadedFile('Name of the django file', f.read())
        course_episode: CourseEpisode = CourseEpisode.objects.create(course=self.course, number=1,
                                                                     title="introduction", duration="02:05:01",
                                                                     video=file)
        url = reverse('course:api:course-episode-detail', kwargs={'pk': course_episode.pk})
        response = self.client.delete(url, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_course_episodes_of_a_course(self):
        with open('course/tests/files/sample.mp4', 'rb') as f:
            file = SimpleUploadedFile('Name of the django file', f.read())
        course_episode1: CourseEpisode = CourseEpisode.objects.create(course=self.course, number=1,
                                                                      title="introduction", duration="02:05:01",
                                                                      video=file)
        course_episode2: CourseEpisode = CourseEpisode.objects.create(course=self.course, number=2,
                                                                      title="introduction2", duration="02:05:01",
                                                                      video=file)
        url = reverse_querystring('course:api:course-episode-list', query_kwargs={'course_sku': self.course.sku})
        response = self.client.get(url, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_episode_count = CourseEpisode.objects.filter(course=self.course).count()
        self.assertEqual(response.data.get('count'), course_episode_count)












