from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from apps.product.models.base import TimeStampedModel
from apps.product.models.Category import Category
from apps.product.models.Unit import Unit
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator

class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(
        max_length=255,
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="products",
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    discount_percentage  = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        default=1.0
    )

    selling_price = models.DecimalField(
    max_digits=12,
    decimal_places=2,  
    null=True,
    blank=True     
)
    description = CKEditor5Field(
        null=True,
        blank=True
        )
    
    is_active = models.BooleanField(
        default=True,
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True,
    )

    class Meta:
        db_table = "products"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if self.cost_price is not None:
            cost = Decimal(str(self.cost_price))
            discount = Decimal(str(self.discount_percentage or 0))
            self.selling_price = (
                cost * (Decimal("100") - discount) / Decimal("100")
            ).quantize(Decimal("0.01"))

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        if is_new:
            self._save_to_default_warehouse()

    def _save_to_default_warehouse(self):
        from apps.inventory.models import Inventory
        from apps.inventory.models.stocklocation import StockLocation

        warehouse = (
            StockLocation.objects
            .filter(is_default=True, is_active=True)
            .order_by("id")
            .first()
        )
        if warehouse is None:
            return

        Inventory.objects.get_or_create(
            product=self,
            location=warehouse,
            defaults={"quantity": self.quantity or 0},
        )

    def __str__(self):
        return self.name
