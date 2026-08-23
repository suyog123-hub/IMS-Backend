from rest_framework import serializers
from apps.product.models.product import Product
class ProductSerializer(serializers.ModelSerializer):
    # integer format ma dekhauxa so string format ma chagne garna ko lagi 
    category_name = serializers.CharField(source="category.name", read_only=True)
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
             "unit",
            "category_name",
            "unit_name",
            "name",
            "slug",
            "quantity",
            "cost_price",
            "discount_percentage",
            "selling_price",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        
        read_only_fields = ["slug", "selling_price"]

    def get_final_price(self, obj):
        return obj.selling_price

    def get_discount_amount(self, obj):
        if obj.cost_price is None or obj.selling_price is None:
            return None
        return obj.cost_price - obj.selling_price

    def get_is_discounted(self, obj):
        return obj.discount_percentage is not None and obj.discount_percentage > 0

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

    def validate_cost_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Cost price cannot be negative.")
        return value

    def validate_discount_percentage(self, value):
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("Discount cannot be negative.")
            if value > 100:
                raise serializers.ValidationError("Discount cannot exceed 100%.")
        return value