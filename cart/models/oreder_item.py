from secrets import token_urlsafe
from django.db import models
from django.contrib.auth import get_user_model
from cms.models.mixins import SkuMixin, TimeStampModelMixin

User = get_user_model()

class OrderItem(SkuMixin, TimeStampModelMixin):
    """
        Intermediary model of Cart and course
        Each cart has several course
        and Each course could be in many carts
    """
    course = models.ForeignKey(
        'course.Course',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='orderitems'
    )
    cart = models.ForeignKey(
        'cart.Cart',
        on_delete=models.CASCADE,
        related_name='orderitems',
        db_index=True,
    )
    price = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='فقط در لحظه ی نهایی شدن سفارش، قیمت ذخیره میشود'
    )

    def __str__(self):
        return f'course "{self.course.sku}" in cart "{self.cart.sku}"'

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = token_urlsafe(16)
        return super(OrderItem, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
