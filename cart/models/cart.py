from secrets import token_urlsafe

from django.db import models
from cms.models.mixins import SkuMixin, TimeStampModelMixin
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderManager(models.Manager):
    def get_queryset(self):
        return super(OrderManager, self).get_queryset().exclude(step='initial')

class Cart(SkuMixin, TimeStampModelMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        db_index=True,
    )

    CART_STEP_CHOICES = (
        ('initial', 'initial'),
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('canceled', 'canceled'),
    )
    step = models.CharField(
        'step',
        max_length=10,
        default='initial',
        choices=CART_STEP_CHOICES,
        db_index=True,
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )
    objects = models.Manager()
    order_objects = OrderManager()

    def __str__(self):
        return f'{self.user} - {self.step}'

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.sku = token_urlsafe(16)
        super().save(*args, **kwargs)
