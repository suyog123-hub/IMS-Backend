from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from apps.product.models.base import TimeStampedModel
from apps.product.models.product import Product
from apps.product.models.product_varient import ProductVariant
from apps.inventory.models.stock_count import StockCount


class StockCountLine(TimeStampedModel):
    stock_count = models.ForeignKey(
        StockCount,
        on_delete=models.CASCADE,
        related_name="lines",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="stock_count_lines",
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_count_lines",
    )
    system_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False,
        help_text="Auto-filled from Inventory",
    )
    counted_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Quantity actually counted physically",
    )
    difference = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        help_text="counted_quantity − system_quantity",
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "stock_count_lines"
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["stock_count", "product", "variant"],
                name="unique_count_line_per_product_variant",
            ),
        ]
        indexes = [
            models.Index(fields=["stock_count"]),
            models.Index(fields=["product"]),
            models.Index(fields=["variant"]),
        ]

    def save(self, *args, **kwargs):
        from apps.inventory.models.inventory import Inventory

        location = self.stock_count.location
        inventory = Inventory.objects.filter(
            product=self.product,
            location=location,
        ).first()
        self.system_quantity = inventory.quantity if inventory else Decimal("0")

        self.difference = self.counted_quantity - self.system_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        variant_str = f" ({self.variant})" if self.variant else ""
        return f"{self.product}{variant_str}: {self.system_quantity} → {self.counted_quantity}"
