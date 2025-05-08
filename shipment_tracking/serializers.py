from rest_framework import serializers
from .models import Transfer, TransferItem, Return, ShipmentTracking, ShipmentItem

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

class TransferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferItem
        fields = '__all__'

class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'

class ShipmentTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentTracking
        fields = '__all__'

class ShipmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentItem
        fields = '__all__'
