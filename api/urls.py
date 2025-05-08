from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'inventory', views.InventoryAndPriceFactViewSet)
router.register(r'products', views.ProductDimViewSet)
router.register(r'dates', views.DateDimViewSet)
router.register(r'stores', views.StoreDimViewSet)
router.register(r'suppliers', views.SupplierDimViewSet)
router.register(r'categories', views.CategoryDimViewSet)
router.register(r'sales', views.SalesFactViewSet)
router.register(r'customers', views.CustomerDimViewSet)
router.register(r'promotions', views.PromotionDimViewSet)
router.register(r'shipping', views.ShippingDimViewSet)
router.register(r'payments', views.PaymentDimViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
