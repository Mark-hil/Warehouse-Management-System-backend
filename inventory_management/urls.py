from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('items', views.ItemViewSet)
router.register('warehouses', views.WarehouseViewSet)
router.register('inventory', views.InventoryViewSet)
router.register('audit', views.InventoryAuditViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
