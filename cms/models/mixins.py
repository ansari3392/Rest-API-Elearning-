from django.db import models


class SkuMixin(models.Model):
    sku = models.CharField(
        max_length=255,
        editable=False,
        unique=True,
        db_index=True,
        null=True,
        default=None
    )

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
