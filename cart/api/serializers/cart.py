from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from cart.api.serializers.order_items import OrderItemSerializer
from cart.models import OrderItem
from cart.models.cart import Cart
from course.models import Course
from utils.func import PersianDateTime


class CartSerializer(ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    total_price = SerializerMethodField()
    created = SerializerMethodField()

    def get_created(self, obj):
        return PersianDateTime(obj.created)

    class Meta:
        model = Cart
        fields = (
            'id',
            'sku',
            'step',
            'created',
            'description',
            'orderitems',
            'total'
            '_price'
        )
        read_only_fields = ('sku',)

    def get_total_price(self, obj):
        return obj.total_price


class AddToCartSerializer(ModelSerializer):
    course = serializers.CharField(allow_null=False, allow_blank=False, required=True)

    def validate_course(self, sku):
        course = get_object_or_404(Course, sku=sku)  # user should send sku of course
        return course

    class Meta:
        model = Cart
        fields = [
           'course'
        ]


class RemoveFromCartSerializer(ModelSerializer):
    order_item = serializers.CharField(allow_null=False, allow_blank=False, required=True)

    def __init__(self, *args, cart=None, **kwargs):  # there is a better way to send cart to serializer (by context)
        super().__init__(*args, **kwargs)
        self.cart = cart

    def validate_order_item(self, sku):
        order_item = get_object_or_404(OrderItem, sku=sku, cart_id=self.cart.id)  # user should send sku of orderitem
        return order_item




    class Meta:
        model = Cart
        fields = [
            'order_item'

        ]


class OrderListSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    total_price = SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'id',
            'sku',
            'user',
            'full_name',
            'paid_at',
            'step',
            'total_price'
        )
        read_only_fields = ('sku', 'paid_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user.get_full_name() else ''

    def get_total_price(self, obj):
        return obj.total_price
