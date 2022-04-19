from secrets import token_urlsafe
import time
from django.db import models
from django.utils.text import slugify

from cms.models.mixins import SkuMixin, TimeStampModelMixin
from django.contrib.auth import get_user_model


User = get_user_model()


class CourseEpisode(SkuMixin, TimeStampModelMixin):
    course = models.ForeignKey(
        'course.Course',
        related_name='episodes',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    number = models.PositiveIntegerField()
    title = models.CharField(
        max_length=500,
        unique=True
    )
    video = models.FileField()
    video_poster = models.ImageField(
        null=True,
        blank=True
    )
    duration = models.DurationField(

    )
    is_free = models.BooleanField(
        default=False
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'Episode {self.number} of {self.course.title}'

    def save(self, *args, **kwargs):

        if not self.sku:
            self.sku = token_urlsafe(16)
        if not self.slug:
            time1 = time.time()
            self.slug = slugify(self.title, allow_unicode=True)
            time2 = time.time()
            time3 = time2 - time1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'course Episode'
        verbose_name_plural = 'course Episodes'
        ordering = ['number']
