from django.db import models
from django.conf import settings
from apps.product.models.base import TimeStampedModel
from apps.inventory.models.stocklocation import StockLocation


class StockCount(TimeStampedModel):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    location = models.ForeignKey(
        StockLocation,
        on_delete=models.PROTECT,
        related_name="stock_counts",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )
    notes = models.TextField(blank=True)
    counted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_counts",
    )

    class Meta:
        db_table = "stock_counts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["location"]),
            models.Index(fields=["counted_by"]),
        ]

    def __str__(self):
        return f"Stock Count #{self.pk} — {self.location} ({self.get_status_display()})"
