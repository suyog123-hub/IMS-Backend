from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from apps.inventory.models.stock_movement import StockMovement
from apps.inventory.serializer.stock_movement import StockMovementSerializer


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related(
        "product", "variant", "location", "created_by"
    ).all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["product__name", "movement_type"]
    ordering_fields = ["movement_type", "created_at"]
