from rest_framework import viewsets, permissions
from .models import ReportItem, MaintenanceHistory
from .serializers import ReportItemSerializer, MaintenanceHistorySerializer

class ReportItemViewSet(viewsets.ModelViewSet):
    queryset = ReportItem.objects.all()
    serializer_class = ReportItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class MaintenanceHistoryViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceHistory.objects.all()
    serializer_class = MaintenanceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
