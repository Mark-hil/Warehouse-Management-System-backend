"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from inventory_management.views import CategoryViewSet, ItemViewSet, WarehouseViewSet, InventoryViewSet, InventoryAuditViewSet
from user_accounts.views import UserViewSet, PermissionViewSet, NotificationViewSet
from sales_management.views import CustomerViewSet, SaleViewSet, PaymentViewSet, PriceHistoryViewSet

router = DefaultRouter()
router.register(r'inventory/categories', CategoryViewSet)
router.register(r'inventory/items', ItemViewSet)
router.register(r'inventory/warehouses', WarehouseViewSet)
router.register(r'inventory/inventory', InventoryViewSet)
router.register(r'inventory/audit', InventoryAuditViewSet)
router.register(r'users', UserViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'price-history', PriceHistoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', permission_classes([AllowAny])(views.obtain_auth_token)),
    path('api/', include(router.urls)),
    path('api/users/', include('user_accounts.urls')),
    path('api/procurement/', include('procurement_system.urls')),
    path('api/shipment/', include('shipment_tracking.urls')),
    path('api/reports/', include('report_management.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/sales/', include('sales_management.urls')),
]
