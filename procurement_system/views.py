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

import logging

logger = logging.getLogger(__name__)

class ProcurementViewSet(viewsets.ModelViewSet):
    serializer_class = ProcurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Procurement.objects.all().prefetch_related('items')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Error listing procurements: {e}')
            return Response({'error': str(e)}, status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Error retrieving procurement: {e}')
            return Response({'error': str(e)}, status=500)

    def update(self, request, *args, **kwargs):
        try:
            logger.info(f'Updating procurement with data: {request.data}')
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info(f'Successfully updated procurement: {serializer.data}')
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Error updating procurement: {e}')
            return Response({'error': str(e)}, status=500)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        try:
            procurement = self.get_object()
            items = ProcurementItem.objects.filter(procurement=procurement)
            serializer = ProcurementItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Error retrieving procurement items: {e}')
            return Response({'error': str(e)}, status=500)

class ProcurementItemViewSet(viewsets.ModelViewSet):
    queryset = ProcurementItem.objects.all()
    serializer_class = ProcurementItemSerializer
    permission_classes = [permissions.IsAuthenticated]
