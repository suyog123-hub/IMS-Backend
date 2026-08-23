from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.product.models.Category import Category
from apps.product.serializer.CategorySerializer import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
