from rest_framework import serializers
from apps.product.models.product import Product
from apps.product.serializer.Category import CategorySerializer
from apps.product.serializer.Unit import UnitSerializer


class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)
    unit_detail = UnitSerializer(source="unit", read_only=True)
    variants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_detail",
            "name",
            "slug",
            "unit",
            "unit_detail",
            "quantity",
            "decription",
            "is_active",
            "variants",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class ProductDetailSerializer(ProductSerializer):
    variants = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_detail",
            "name",
            "slug",
            "unit",
            "unit_detail",
            "quantity",
            "decription",
            "is_active",
            "variants",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def get_variants(self, obj):
        return [
            {
                "id": v.id,
                "name": v.name,
                "cost_price": v.cost_price,
                "selling_price": v.selling_price,
                "is_active": v.is_active,
            }
            for v in obj.variants.all()
        ]
