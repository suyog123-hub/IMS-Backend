from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.product.models.base import TimeStampedModel
from apps.product.models.product import Product
from apps.product.models.product_varient import ProductVariant
from apps.inventory.models.stocklocation import StockLocation
from apps.inventory.models.inventory import Inventory


class StockMovement(TimeStampedModel):

    MOVEMENT_TYPES = [
        ("receive", "Receive"),
        ("sale", "Sale"),
        ("return", "Return"),
        ("adjustment", "Adjustment"),
        ("transfer_in", "Transfer In"),
        ("transfer_out", "Transfer Out"),
        ("damaged", "Damaged"),
    ]

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.PROTECT,
        related_name="movements",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="stock_movements",
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
    )
    location = models.ForeignKey(
        StockLocation,
        on_delete=models.PROTECT,
        related_name="stock_movements",
    )
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES,
    )
    quantity_change = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Positive for incoming, negative for outgoing",
    )
    reference_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. purchase_order, order, stock_transfer",
    )
    reference_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of the related record",
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
    )

    class Meta:
        db_table = "stock_movements"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["variant"]),
            models.Index(fields=["location"]),
            models.Index(fields=["movement_type"]),
            models.Index(fields=["reference_type", "reference_id"]),
            models.Index(fields=["created_by"]),
        ]

    def __str__(self):
        direction = "+" if self.quantity_change >= 0 else ""
        return (
            f"{self.get_movement_type_display()}: "
            f"{self.product} {direction}{self.quantity_change} @ {self.location}"
        )
