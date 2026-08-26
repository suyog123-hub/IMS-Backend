from rest_framework import serializers
from apps.inventory.models.stock_movement import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    variant_name = serializers.CharField(source="variant.name", read_only=True, default=None)
    location_name = serializers.CharField(source="location.name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.username", read_only=True, default=None)

    class Meta:
        model = StockMovement
        fields = [
            "id", "inventory", "product", "product_name", "variant",
            "variant_name", "location", "location_name", "movement_type",
            "quantity_change", "reference_type", "reference_id",
            "notes", "created_by", "created_by_name", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
