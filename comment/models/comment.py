from secrets import token_urlsafe

from django.db import models
from django.contrib.auth import get_user_model
from cms.models import SkuMixin, TimeStampModelMixin
from Blog.models.article import Article
from course.models.course import Course

User = get_user_model()

class Comment(SkuMixin, TimeStampModelMixin):
    article = models.ForeignKey(
        Article,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    course = models.ForeignKey(
        Course,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    description = models.TextField(
    )

    is_private = models.BooleanField(
        default=False

    )
    is_active = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = token_urlsafe(16)
        super(Comment, self).save(*args, **kwargs)








