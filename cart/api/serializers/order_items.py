from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from khayyam import JalaliDatetime
from pytz import timezone
from django.contrib.auth import get_user_model
from cart.models import OrderItem

User = get_user_model()


class OrderItemSerializer(ModelSerializer):
    course_title = SerializerMethodField()
    live_price = SerializerMethodField()
    created = SerializerMethodField()

    def get_created(self, obj):
        date = JalaliDatetime(
            obj.created.astimezone(tz=timezone('Asia/Tehran'))
        )
        return str(date)

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


