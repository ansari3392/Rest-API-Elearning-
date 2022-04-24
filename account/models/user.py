
import secrets

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from cms.models.mixins import SkuMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone_number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(SkuMixin, AbstractUser):
    username = None
    password = models.CharField("password", max_length=128, null=True, blank=True)
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
    is_verified = models.BooleanField(default=False)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number) if self.phone_number else str(self.email)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(16)
        if self.email == '':
            self.email = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
