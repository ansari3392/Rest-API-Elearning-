from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from django.template.defaultfilters import safe
from django.urls import reverse
from django.utils.text import slugify
from cms.models.mixins import SkuMixin, TimeStampModelMixin

User = get_user_model()

class Category(MPTTModel, SkuMixin, TimeStampModelMixin):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=255,
        null=True,
    )
    slug = models.SlugField(
        null=True,
        blank=True,
    )

    svg = models.FileField(
        'SVG',
        null=True,
        blank=True,
        upload_to='categories/',
        validators=[FileExtensionValidator(['svg'])],
    )
    order = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['order']

    def get_svg_code(self):
        return safe(str(self.svg.read(), encoding='utf-8')) if self.svg else ''

    def get_svg_url(self):
        return self.svg.url if self.svg else ''


