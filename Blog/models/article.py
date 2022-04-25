from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from secrets import token_urlsafe
from django.utils.text import slugify
from cms.models.mixins import SkuMixin, TimeStampModelMixin
from cms.models.tag import Tag

User = get_user_model()

class Article(SkuMixin, TimeStampModelMixin):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, allow_unicode=True)
    description = models.TextField()
    main_image = models.ImageField(
        null=True,
        blank=True
    )
    image = models.ImageField(
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    is_published = models.BooleanField(default=False)
    category = models.CharField(max_length=250, default='coding')
    viewed = models.IntegerField(
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='article_tags',
        blank=True,
    )

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = token_urlsafe(16)
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Article, self).save(*args, **kwargs)
