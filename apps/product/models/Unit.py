from django.db import models
from django.core.validators import MinValueValidator
from apps.product.models.base import TimeStampedModel

class Unit(TimeStampedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    class Meta:
        db_table = "units"
        ordering = ["name"]

    def __str__(self):
        return self.name