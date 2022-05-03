from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from cart.models import Cart, OrderItem
from cart.tests.service import create_user
from categories.models import Category
from course.models import Course

User = get_user_model()


class OrdersTest(APITestCase):
    def setUp(self):
        self.user = create_user('09224282993')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        cat = Category.objects.create(title="programming")
        self.course = Course.objects.create(title="testing", description="testing again", teacher=self.user,
                                            category=cat)
        self.order1 = Cart.objects.create(user=self.user, step="paid")
        self.order1.orderitems.create(course=self.course, price='1000')
        self.order2 = Cart.objects.create(user=self.user, step="canceled")
        self.order2.orderitems.create(course=self.course, price='2000')
        self.order3 = Cart.objects.create(user=self.user, step="pending")
        self.order3.orderitems.create(course=self.course, price='3000')

    def test_get_orders_list_success(self):
        url = reverse('cart:api:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 3)
        order = response.data.get('results')[0]
        self.assertEqual(order.get('step'), self.order1.step)
        total_price = sum([item.price for item in self.order1.orderitems.all()])
        self.assertEqual(order.get('total_price'), total_price)

    def test_get_orders_list_unauthorized_fail(self):
        self.client.logout()
        url = reverse('cart:api:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_detail_success(self):
        url = reverse('cart:api:order_detail', kwargs={'pk': self.order1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('step'), self.order1.step)
        total_price = sum([item.price for item in self.order1.orderitems.all()])
        self.assertEqual(response.data.get('total_price'), total_price)
        self.assertEqual(len(response.data.get('orderitems')), self.order1.orderitems.count())
        order_item = response.data.get('orderitems')[0]
        self.assertEqual(order_item.get('course_title'), self.course.title)

    def test_get_orders_detail_unauthorized_fail(self):
        self.client.logout()
        url = reverse('cart:api:order_detail', kwargs={'pk': self.order1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
