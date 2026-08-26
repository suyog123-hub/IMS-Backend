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
    list_display = ("id", "name", "code", "location_type", "phone", "is_active", "created_at")
    list_filter = ("is_active", "location_type")
    search_fields = ("name", "code")
    ordering = ("name",)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "location", "quantity", "created_at")
    search_fields = ("product__name", "location__name")
    ordering = ("-created_at",)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "location", "movement_type", "quantity_change", "created_by", "created_at")
    list_filter = ("movement_type",)
    search_fields = ("product__name",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


class StockCountLineInline(admin.TabularInline):
    model = StockCountLine
    extra = 1
    fields = ("product", "variant", "system_quantity", "counted_quantity", "difference", "notes")
    readonly_fields = ("difference",)


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ("id", "reference_number", "from_location", "to_location", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("reference_number",)
    ordering = ("-created_at",)
    readonly_fields = ("reference_number", "created_at", "updated_at")


@admin.register(StockCount)
class StockCountAdmin(admin.ModelAdmin):
    list_display = ("id", "location", "status", "counted_by", "created_at")
    list_filter = ("status",)
    search_fields = ("location__name",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [StockCountLineInline]


@admin.register(StockCountLine)
class StockCountLineAdmin(admin.ModelAdmin):
    list_display = ("id", "stock_count", "product", "variant", "system_quantity", "counted_quantity", "difference")
    search_fields = ("product__name",)
    readonly_fields = ("difference",)
