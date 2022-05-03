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


class CartTest(APITestCase):
    def setUp(self):
        self.user = create_user('09224282993')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        cat = Category.objects.create(title="programming")
        self.course1 = Course.objects.create(title="testing", description="testing again", teacher=self.user,
                                             category=cat, price='58000')
        self.course2 = Course.objects.create(title="test", description="testing", teacher=self.user,
                                             category=cat, price='1000')
        self.cart = Cart.objects.filter(user=self.user, step="initial").first()

    def test_initial_cart_creation_after_registration(self):
        self.assertTrue(Cart.objects.filter(user=self.user, step='initial').first())
        self.assertEqual(Cart.objects.filter(user=self.user, step='initial').count(), 1)

    def test_get_cart_detail_by_owner(self):
        self.cart.orderitems.create(course=self.course1)
        self.cart.orderitems.create(course=self.course2)
        url = reverse('cart:api:cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('step'), 'initial')
        self.assertEqual(response.data.get('id'), self.cart.id)
        self.assertEqual(response.data.get('description'), self.cart.description)
        self.assertEqual(len(response.data.get('orderitems')), self.cart.orderitems.count())
        total_price = sum([item.course.price for item in self.cart.orderitems.all()])
        self.assertEqual(response.data.get('total_price'), total_price)

    def test_add_to_cart_by_owner(self):
        url = reverse('cart:api:add_or_remove_from_cart')
        data = {
            'course': self.course1.sku,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_items_count = self.cart.orderitems.count()
        self.assertEqual(order_items_count, 1)

    def test_add_course_again_fail(self):
        self.cart.orderitems.create(course=self.course1)
        url = reverse('cart:api:add_or_remove_from_cart')
        data = {
            'course': self.course1.sku,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_order_item_by_owner(self):
        order_item = OrderItem.objects.create(cart=self.cart, course=self.course1)
        url = reverse('cart:api:add_or_remove_from_cart')
        data = {
            'order_item': order_item.sku,
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        order_items_count = self.cart.orderitems.count()
        self.assertEqual(order_items_count, 0)

    def test_remove_order_item_from_other_carts(self):
        pass
