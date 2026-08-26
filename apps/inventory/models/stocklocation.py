# apps/inventory/models.py
from django.db import models
from apps.product.models.base import TimeStampedModel

class StockLocation(TimeStampedModel):
    """
    Physical or virtual location where stock is stored.
    """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    LOCATION_TYPES = [
        ('warehouse', 'Warehouse'),
        ('store', 'Store'),
        ('shop', 'Shop'),
        ('godown', 'Godown'),
        ('virtual', 'Virtual'),
        ('shelf', 'Shelf'),
        ('rack', 'Rack'),
        ('bin', 'Bin'),
        ('cold_storage', 'Cold Storage'),
        ('showroom', 'Showroom'),
    ]
    location_type = models.CharField(
        max_length=50,
        choices=LOCATION_TYPES,
        default='warehouse',
    )
    description = models.TextField(blank=True,help_text="Additional details about this location")
    code = models.CharField(max_length=20,unique=True,help_text="Example: WH-01, STR-02, SH-ELEC-01")
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "stock_locations"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["location_type"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["parent"]),
        ]
        verbose_name = "Stock Location"
        verbose_name_plural = "Stock Locations"
    
    def __str__(self):
        return self.name