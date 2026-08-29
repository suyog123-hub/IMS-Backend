from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from apps.product.models.product import Product
from apps.product.serializer.product import (
    ProductSerializer,
)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "unit").all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "quantity", "created_at"]
    
    @method_decorator(cache_page(20))  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
