from django.contrib import admin

from apps.product.models import Category, Product, ProductVariant, Unit


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ("name", "cost_price", "selling_price", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "category",
        "unit",
        "quantity",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "category", "unit")
    search_fields = ("name", "slug")
    ordering = ("name",)
    readonly_fields = ("slug", "created_at", "updated_at")
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "product",
        "cost_price",
        "selling_price",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "product")
    search_fields = ("name", "product__name")
