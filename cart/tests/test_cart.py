from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from cart.models import Cart
from cart.tests.service import create_user
from categories.models import Category
from course.models import Course

User = get_user_model()

class CartTest(APITestCase):
    def setUp(self):
        self.user = create_user('mahtab', 'mahtab@gmail.com')
        refresh = RefreshToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        cat = Category.objects.create(title="programming")
        self.course = Course.objects.create(title="testing", description="testing again", teacher=self.user,
                                            category=cat)
        self.cart = Cart.objects.filter(user=self.user, step="initial").first()

    def test_initial_cart_creation_after_registration(self):
        self.assertTrue(Cart.objects.filter(user=self.user, step='initial').first())
        self.assertEqual(Cart.objects.filter(user=self.user, step='initial').count(), 1)

    def test_get_cart_detail_by_owner(self):
        url = reverse('cart:api:cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart_by_owner(self):
        url = reverse('cart:api:add_or_remove_from_cart')
        data = {
            'course': self.course.sku,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_items_count = self.cart.orderitems.count()
        self.assertEqual(order_items_count, 1)


    def test_add_to_cart_by_non_owner(self):
        pass

    def test_add_course_only_one_time(self):
        pass

    def test_remove_order_item_by_owner(self):
        pass

    def test_remove_order_item_by_non_owner(self):
        pass

    def test_remove_order_item_from_other_carts(self):
        pass

