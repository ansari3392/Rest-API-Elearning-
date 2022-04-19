from secrets import token_urlsafe

from django.db import models
from cms.models.mixins import SkuMixin, TimeStampModelMixin
from django.contrib.auth import get_user_model
from course.models import Course

User = get_user_model()


class Favorite(SkuMixin, TimeStampModelMixin):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    def __str__(self):
        return f'{self.author} added {self.course} to favorites'

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = token_urlsafe(16)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

