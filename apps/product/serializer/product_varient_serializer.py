from rest_framework import serializers
from apps.product.models.product_varient import ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "product_name",
            "name",
            "is_active",
            "cost_price",
            "selling_price",     
            "discount_percentage",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["selling_price"]


    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
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


    def validate(self, data):
        cost_price = data.get("cost_price")
        discount_percentage = data.get("discount_percentage")
        if cost_price is not None and discount_percentage is not None:
            if discount_percentage > 0 and cost_price == 0:
                raise serializers.ValidationError(
                    "Cannot apply a discount to a product with zero cost."
                )

        return data