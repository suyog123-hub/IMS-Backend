from decimal import Decimal

from django.db import models
from django.conf import settings
from apps.product.models.base import TimeStampedModel
from apps.product.models.product import Product
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
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="transfers",
        null=True,
        blank=True,
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
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

    def save(self, *args, **kwargs):
        if not self.reference_number:
            last = StockTransfer.objects.order_by("-pk").first()
            num = (last.pk + 1) if last else 1
            self.reference_number = f"TRF-{num:05d}"

        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new and self.product and self.quantity:
            from apps.inventory.models.stock_movement import StockMovement

            StockMovement.objects.create(
                product=self.product,
                location=self.from_location,
                movement_type="transfer_out",
                quantity_change=-self.quantity,
                reference_type="stock_transfer",
                reference_id=self.pk,
                created_by=self.created_by,
                notes=f"Transfer {self.reference_number} out",
            )
            StockMovement.objects.create(
                product=self.product,
                location=self.to_location,
                movement_type="transfer_in",
                quantity_change=self.quantity,
                reference_type="stock_transfer",
                reference_id=self.pk,
                created_by=self.created_by,
                notes=f"Transfer {self.reference_number} in",
            )

    def __str__(self):
        return f"{self.reference_number}: {self.from_location} → {self.to_location}"
