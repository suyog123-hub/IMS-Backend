from rest_framework import serializers
from apps.inventory.models.stock_count import StockCount
from apps.inventory.models.stock_count_line import StockCountLine


class StockCountLineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    variant_name = serializers.CharField(source="variant.name", read_only=True, default=None)

    class Meta:
        model = StockCountLine
        fields = [
            "id", "product", "product_name", "variant", "variant_name",
            "system_quantity", "counted_quantity", "difference", "notes",
        ]
        read_only_fields = ["id", "difference"]


class StockCountSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source="location.name", read_only=True)
    counted_by_name = serializers.CharField(source="counted_by.username", read_only=True, default=None)
    lines = StockCountLineSerializer(many=True, read_only=True)

    class Meta:
        model = StockCount
        fields = [
            "id", "location", "location_name", "status", "notes",
            "counted_by", "counted_by_name", "lines", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
