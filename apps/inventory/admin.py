from django.contrib import admin
from apps.inventory.models import (
    StockLocation,
    Inventory,
    StockMovement,
    StockTransfer,
    StockCount,
    StockCountLine,
)
@admin.register(StockLocation)
class StockLocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "location_type", "phone", "is_active", "is_default", "updated_at")
    list_filter = ("is_active", "location_type", "is_default")
    search_fields = ("name", "code")
    ordering = ("-id",)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "location", "quantity", "updated_at")
    search_fields = ("product__name", "location__name")
    ordering = ("-id",)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "location", "movement_type", "quantity_change", "created_by", "updated_at")
    list_filter = ("movement_type",)
    search_fields = ("product__name",)
    ordering = ("-id",)
    readonly_fields = ("updated_at", "updated_at")


class StockCountLineInline(admin.TabularInline):
    model = StockCountLine
    extra = 1
    fields = ("product", "variant", "system_quantity", "counted_quantity", "difference", "notes")
    readonly_fields = ("system_quantity", "difference",)


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ("id", "reference_number", "product", "quantity", "from_location", "to_location", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("reference_number", "product__name")
    ordering = ("-id",)
    readonly_fields = ("reference_number", "updated_at", "updated_at")


@admin.register(StockCount)
class StockCountAdmin(admin.ModelAdmin):
    list_display = ("id", "location", "status", "counted_by", "updated_at")
    list_filter = ("status",)
    search_fields = ("location__name",)
    ordering = ("-id",)
    readonly_fields = ("updated_at", "updated_at")
    inlines = [StockCountLineInline]


@admin.register(StockCountLine)
class StockCountLineAdmin(admin.ModelAdmin):
    list_display = ("id", "stock_count", "product", "variant", "system_quantity", "counted_quantity", "difference")
    search_fields = ("product__name",)
    readonly_fields = ("system_quantity", "difference",)
