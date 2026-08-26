from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from apps.inventory.models.stock_count import StockCount
from apps.inventory.models.stock_count_line import StockCountLine
from apps.inventory.serializer.stock_count import StockCountSerializer, StockCountLineSerializer


class StockCountViewSet(viewsets.ModelViewSet):
    queryset = StockCount.objects.select_related("location", "counted_by").prefetch_related("lines__product", "lines__variant").all()
    serializer_class = StockCountSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["location__name"]
    ordering_fields = ["status", "created_at"]


class StockCountLineViewSet(viewsets.ModelViewSet):
    queryset = StockCountLine.objects.select_related("stock_count", "product", "variant").all()
    serializer_class = StockCountLineSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ["product", "created_at"]
