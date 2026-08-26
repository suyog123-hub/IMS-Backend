from django.db import models
from django.conf import settings
from apps.product.models.base import TimeStampedModel
from apps.inventory.models.stocklocation import StockLocation


class StockTransfer(TimeStampedModel):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_transit", "In Transit"),
        ("received", "Received"),
        ("cancelled", "Cancelled"),
    ]

    reference_number = models.CharField(
        max_length=50,
        unique=True,
    )
    from_location = models.ForeignKey(
        StockLocation,
        on_delete=models.PROTECT,
        related_name="outgoing_transfers",
    )
    to_location = models.ForeignKey(
        StockLocation,
        on_delete=models.PROTECT,
        related_name="incoming_transfers",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_transfers",
    )

    class Meta:
        db_table = "stock_transfers"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["reference_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["from_location"]),
            models.Index(fields=["to_location"]),
            models.Index(fields=["created_by"]),
        ]

    def __str__(self):
        return f"{self.reference_number}: {self.from_location} → {self.to_location}"
