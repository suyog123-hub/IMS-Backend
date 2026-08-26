from rest_framework import serializers
from apps.inventory.models.inventory import Inventory


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    location_name = serializers.CharField(source="location.name", read_only=True)

    class Meta:
        model = Inventory
        fields = ["id", "product", "product_name", "location", "location_name", "quantity", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
