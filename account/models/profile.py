import secrets

from django.conf import settings
from django.db import models

from cms.models.mixins import SkuMixin, TimeStampModelMixin

User = settings.AUTH_USER_MODEL


class Profile(SkuMixin, TimeStampModelMixin):
    CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    gender = models.CharField(
        null=True,
        max_length=15,
        choices=CHOICES,
    )
    avatar = models.ImageField(
        null=True,
        blank=True
    )
    bio = models.TextField(
        null=True,
        blank=True
    )
    is_teacher = models.BooleanField(
        default=False
    )
    is_consultant = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)

    def get_avatar_url(self):
        return self.avatar.url if self.avatar else ''
