from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'purchases', views.PurchaseViewSet)
router.register(r'purchase-items', views.PurchaseItemViewSet)
router.register(r'procurement', views.ProcurementViewSet)
router.register(r'procurement-items', views.ProcurementItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
