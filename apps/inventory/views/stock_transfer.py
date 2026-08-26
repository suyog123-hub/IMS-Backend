from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from apps.inventory.models.stock_transfer import StockTransfer
from apps.inventory.serializer.stock_transfer import StockTransferSerializer


class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.select_related(
        "from_location", "to_location", "created_by"
    ).all()
    serializer_class = StockTransferSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["reference_number"]
    ordering_fields = ["status", "created_at"]
