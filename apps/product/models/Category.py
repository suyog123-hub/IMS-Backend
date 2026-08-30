from django.db import models
from apps.product.models.base import TimeStampedModel

class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-id']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
