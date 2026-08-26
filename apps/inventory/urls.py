from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.inventory.views import (
    StockLocationViewSet,
    InventoryViewSet,
    StockMovementViewSet,
    StockTransferViewSet,
    StockCountViewSet,
    StockCountLineViewSet,
)
router = DefaultRouter()
router.register("locations", StockLocationViewSet, basename="stock-location")
router.register("inventory", InventoryViewSet, basename="inventory")
router.register("movements", StockMovementViewSet, basename="stock-movement")
router.register("transfers", StockTransferViewSet, basename="stock-transfer")
router.register("counts", StockCountViewSet, basename="stock-count")
router.register("count-lines", StockCountLineViewSet, basename="stock-count-line")

urlpatterns = [
    path("", include(router.urls)),
]
