from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from apps.inventory.models.inventory import Inventory
from apps.inventory.serializer.inventory import InventorySerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related("product", "location").all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["product__name"]
    ordering_fields = ["quantity", "created_at"]
