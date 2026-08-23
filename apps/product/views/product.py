from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.product.models.product import Product
from apps.product.serializer.product import (
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "unit").all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "quantity", "created_at"]

 
