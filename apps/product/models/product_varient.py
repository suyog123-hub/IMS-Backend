from django.db import models
from apps.product.models.base import TimeStampedModel
from apps.product.models.product import Product

class ProductVariant(TimeStampedModel):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    name = models.CharField(
        max_length=255,
        help_text="Example: Black / Medium",
    )

    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "product_variants"
        ordering = ["product__name", "name"]
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["is_active"]),
        ]


    def __str__(self):
        return self.name