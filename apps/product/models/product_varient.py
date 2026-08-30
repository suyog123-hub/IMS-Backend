from decimal import Decimal

from django.db import models
from apps.product.models.base import TimeStampedModel
from apps.product.models.product import Product
from django.core.validators import MinValueValidator
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

    discount_percentage  = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    selling_price = models.DecimalField(
    max_digits=12,
    decimal_places=2,       
    null=True,
    blank=True
)

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "product_variants"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):
        if self.cost_price is not None:
            cost = Decimal(str(self.cost_price))
            discount = Decimal(str(self.discount_percentage or 0))
            self.selling_price = (
                cost * (Decimal("100") - discount) / Decimal("100")
            ).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name