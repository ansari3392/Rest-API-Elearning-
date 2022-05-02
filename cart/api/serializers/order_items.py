from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from cart.models import OrderItem
from utils.func import PersianDateTime

User = get_user_model()


class OrderItemSerializer(ModelSerializer):
    course_title = SerializerMethodField()
    live_price = SerializerMethodField()
    created = SerializerMethodField()

    def get_created(self, obj):
        return PersianDateTime(obj.created)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'sku',
            'course_title',
            'live_price'
        )
        read_only_fields = ('sku', )

    def get_course_title(self, obj):
        return obj.course.title if obj.course.title else ''

    def get_live_price(self, obj):
        return obj.live_price


