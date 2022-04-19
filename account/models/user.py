
import secrets
from django.contrib.auth.models import AbstractUser
from django.db import models
from cms.models.mixins import SkuMixin

class CustomUser(SkuMixin, AbstractUser):
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        error_messages={
            'unique': "A user with that phone number already exists.",
        },
        null=True,
        blank=True,
    )
    email = models.EmailField(
        null=True,
        unique=True,
        blank=True
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(16)
        if self.email == '':
            self.email = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
