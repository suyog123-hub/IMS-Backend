from django.db import models
from apps.product.models.base import TimeStampedModel
from apps.product.models.product import Product
from apps.inventory.models.stocklocation import StockLocation


class Inventory(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="inventory_records")
    location = models.ForeignKey(StockLocation, on_delete=models.PROTECT, related_name="inventories")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "inventory"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["product", "location"], name="unique_inventory_per_product_location"),
        ]

    def __str__(self):
        return f"{self.product} @ {self.location}: {self.quantity}"
