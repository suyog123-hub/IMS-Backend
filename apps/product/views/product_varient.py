from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.product.models.product_varient import ProductVariant
from apps.product.serializer.product_varient import ProductVariantSerializer


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.select_related("product").all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "product__name"]
    ordering_fields = ["name", "cost_price", "selling_price", "created_at"]
