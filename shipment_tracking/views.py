from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transfer, TransferItem, Return, ShipmentTracking, ShipmentItem
from .serializers import (
    TransferSerializer, TransferItemSerializer, ReturnSerializer,
    ShipmentTrackingSerializer, ShipmentItemSerializer
)

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        transfer = self.get_object()
        items = TransferItem.objects.filter(transfer=transfer)
        serializer = TransferItemSerializer(items, many=True)
        return Response(serializer.data)

class TransferItemViewSet(viewsets.ModelViewSet):
    queryset = TransferItem.objects.all()
    serializer_class = TransferItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShipmentTrackingViewSet(viewsets.ModelViewSet):
    queryset = ShipmentTracking.objects.all()
    serializer_class = ShipmentTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        shipment = self.get_object()
        items = ShipmentItem.objects.filter(shipment=shipment)
        serializer = ShipmentItemSerializer(items, many=True)
        return Response(serializer.data)

class ShipmentItemViewSet(viewsets.ModelViewSet):
    queryset = ShipmentItem.objects.all()
    serializer_class = ShipmentItemSerializer
    permission_classes = [permissions.IsAuthenticated]
