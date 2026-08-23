from rest_framework.routers import DefaultRouter
from django.urls import path , include
from apps.product.views import (
    CategoryViewSet,
    ProductVariantViewSet,
    ProductViewSet,
    UnitViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("units", UnitViewSet, basename="unit")
router.register("products", ProductViewSet, basename="product")
router.register("variants", ProductVariantViewSet, basename="product-variant")

urlpatterns = [
    path('', include(router.urls)),
]
