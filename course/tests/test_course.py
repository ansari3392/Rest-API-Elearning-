from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import Profile
from categories.models import Category
from cms.models import Tag
from course.models import Course
from course.tests.service import create_admin, create_teacher

User = get_user_model()


class CourseTest(APITestCase):
    def setUp(self):
        self.user = create_admin('09224282994')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.user2 = create_teacher("09224282995", 'mahtab')
        Profile.objects.filter(user=self.user2).update(is_teacher=True)
        self.cat1 = Category.objects.create(title="programming")
        self.tag1 = Tag.objects.create(name="coding")
        self.tag2 = Tag.objects.create(name="learning")

    def test_create_course_by_admin_without_cat_success(self):
        url = reverse('course:api:course-list')
        data = {
            "title": "testing",
            "description": "testing",
            "teacher": "mahtab",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'testing')
        self.assertEqual(response.data.get('description'), 'testing')
        self.assertEqual(response.data.get('teacher'), 'mahtab')
        self.assertEqual(response.data.get('category'), None)
        self.assertFalse(response.data.get('is_free'))

    def test_create_course_by_admin_with_cat_success(self):
        url = reverse('course:api:course-list')
        data = {
            "title": "testing",
            "description": "testing",
            "teacher": "mahtab",
            "category": "programming"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'testing')
        self.assertEqual(response.data.get('category'), 'programming')

    def test_create_course_by_admin_with_tag_success(self):
        url = reverse('course:api:course-list')
        data = {
            "title": "testing",
            "description": "testing",
            "teacher": "mahtab",
            "category": "programming",
            "tag_list": ["coding"]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'testing')
        self.assertEqual(len(response.data.get('tags')), 1)

    def test_create_course_by_non_admin_fail(self):
        self.client.logout()
        refresh = RefreshToken.for_user(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('course:api:course-list')
        data = {
            "title": "testing",
            "description": "testing",
            "teacher": "mahtab",
            "category": "programming",
            "tag_list": ["coding"]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_by_admin_success(self):
        course: Course = Course.objects.create(title="testing", description="testing again", teacher=self.user2,
                                               category=self.cat1, )
        course.tags.set([self.tag2, self.tag1])
        url = reverse('course:api:course-detail',  kwargs={'pk': course.pk})
        data = {
            "title": "testing2",

        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), "testing2")
        self.assertEqual(response.data.get("description"), course.description)
        self.assertEqual(response.data.get("id"), course.id)
        self.assertEqual(response.data.get("category"), course.category.title)
        self.assertEqual(len(response.data.get("tags")), 2)

    def test_remove_course_by_admin_success(self):
        course: Course = Course.objects.create(title="testing", description="testing again", teacher=self.user2,
                                               category=self.cat1, )
        course.tags.set([self.tag2, self.tag1])
        url = reverse('course:api:course-detail',  kwargs={'pk': course.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_a_course_detail_success_success(self):
        self.client.logout()
        course: Course = Course.objects.create(title="testing", description="testing again", teacher=self.user2,
                                               category=self.cat1, )
        course.tags.set([self.tag2, self.tag1])
        url = reverse('course:api:course-detail',  kwargs={'pk': course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), course.title)
        self.assertEqual(response.data.get('sku'), course.sku)
        self.assertEqual(response.data.get('is_free'), course.is_free)
        self.assertEqual(response.data.get('price'), course.price)
        self.assertEqual(response.data.get('published_date'), course.published_date)
        self.assertEqual(response.data.get('description'), course.description)
        self.assertEqual(response.data.get('teacher'), course.teacher.id)
        self.assertEqual(response.data.get('category'), course.category.title)
        self.assertEqual(len(response.data.get('episodes')), course.episodes.count())

    def test_get_list_of_courses_success(self):
        course1: Course = Course.objects.create(title="testing", description="testing again", teacher=self.user2,
                                                category=self.cat1, )
        course2: Course = Course.objects.create(title="testing2", description="testing again", teacher=self.user2,
                                                category=self.cat1, )
        course1.tags.set([self.tag2, self.tag1])
        url = reverse('course:api:course-list', )
        response = self.client.get(url)
        course_count = Course.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), course_count)
        course = response.data.get('results')[0]
        self.assertEqual(course.get('title'), course1.title)
        self.assertEqual(course.get('sku'), course1.sku)
        self.assertEqual(course.get('is_free'), course1.is_free)
        self.assertEqual(course.get('price'), course1.price)
        self.assertEqual(course.get('published_date'), course1.published_date)
        self.assertEqual(course.get('description'), course1.description)
        self.assertEqual(course.get('teacher'), course1.teacher.id)
        self.assertEqual(course.get('category'), course1.category.title)
        self.assertEqual(len(course.get('episodes')), course1.episodes.count())
