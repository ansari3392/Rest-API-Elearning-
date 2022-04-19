import secrets

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from cms.models.mixins import SkuMixin, TimeStampModelMixin
from cms.models import Tag
from categories.models.category import Category

User = get_user_model()


class Course(SkuMixin, TimeStampModelMixin):
    title = models.CharField(
        max_length=255,
        unique=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    main_mage = models.ImageField(
        null=True,
        blank=True,

    )
    image = models.ImageField(
        null=True,
        blank=True
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='instructed_courses',
    )

    users = models.ManyToManyField(
        User,
        related_name='bought_courses',
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        related_name='categories',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_free = models.BooleanField(
        default=False
    )
    has_discount = models.BooleanField(
        default=False
    )
    price = models.IntegerField(
        null=True,
        blank=True

    )
    pre_sale = models.BooleanField(
        default=False
    )
    published_date = models.DateTimeField(
        null=True,
        blank=True
    )

    slug = models.SlugField(
        blank=True,
        db_index=True,
        unique=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='courses',
        blank=True
    )

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(16)
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


