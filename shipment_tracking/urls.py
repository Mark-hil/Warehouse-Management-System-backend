from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'transfers', views.TransferViewSet)
router.register(r'transfer-items', views.TransferItemViewSet)
router.register(r'returns', views.ReturnViewSet)
router.register(r'shipments', views.ShipmentTrackingViewSet)
router.register(r'shipment-items', views.ShipmentItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
