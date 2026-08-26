from rest_framework import serializers
from apps.inventory.models.stock_transfer import StockTransfer


class StockTransferSerializer(serializers.ModelSerializer):
    from_location_name = serializers.CharField(source="from_location.name", read_only=True)
    to_location_name = serializers.CharField(source="to_location.name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.username", read_only=True, default=None)

    class Meta:
        model = StockTransfer
        fields = [
            "id", "reference_number", "from_location", "from_location_name",
            "to_location", "to_location_name", "status", "notes",
            "created_by", "created_by_name", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "reference_number", "created_at", "updated_at"]
