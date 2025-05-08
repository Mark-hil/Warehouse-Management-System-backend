from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Supplier, Purchase, PurchaseItem, Procurement, ProcurementItem
from .serializers import (
    SupplierSerializer,
    PurchaseSerializer,
    PurchaseItemSerializer,
    ProcurementSerializer,
    ProcurementItemSerializer
)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        purchase = self.get_object()
        items = PurchaseItem.objects.filter(purchase=purchase)
        serializer = PurchaseItemSerializer(items, many=True)
        return Response(serializer.data)

class PurchaseItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProcurementViewSet(viewsets.ModelViewSet):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        procurement = self.get_object()
        items = ProcurementItem.objects.filter(procurement=procurement)
        serializer = ProcurementItemSerializer(items, many=True)
        return Response(serializer.data)

class ProcurementItemViewSet(viewsets.ModelViewSet):
    queryset = ProcurementItem.objects.all()
    serializer_class = ProcurementItemSerializer
    permission_classes = [permissions.IsAuthenticated]
