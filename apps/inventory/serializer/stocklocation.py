from rest_framework import serializers
from apps.inventory.models.stocklocation import StockLocation


class StockLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLocation
        fields = [
            "id", "name", "code", "location_type", "phone",
            "description", "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value

    def validate_code(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Code must be at least 2 characters long.")
        return value
