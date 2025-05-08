from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reports', views.ReportItemViewSet)
router.register(r'maintenance', views.MaintenanceHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
