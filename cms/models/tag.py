import secrets

from django.db import models
from django.utils.text import slugify

from cms.models import SkuMixin, TimeStampModelMixin


class Tag(SkuMixin, TimeStampModelMixin):
    name = models.CharField(
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(16)
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

