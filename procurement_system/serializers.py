from rest_framework import serializers
from .models import Supplier, Purchase, PurchaseItem, Procurement, ProcurementItem

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = '__all__'

class ProcurementItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcurementItem
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'

class ProcurementSerializer(serializers.ModelSerializer):
    items = ProcurementItemSerializer(many=True, read_only=True)

    class Meta:
        model = Procurement
        fields = '__all__'

class ProcurementItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcurementItem
        fields = '__all__'
