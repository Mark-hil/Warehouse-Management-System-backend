from rest_framework import serializers
from django.contrib.auth import get_user_model
from inventory_management.models import Item
from inventory_management.serializers import ItemSerializer
from .models import Supplier, Purchase, PurchaseItem, Procurement, ProcurementItem

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
    item_details = ItemSerializer(source='item', read_only=True)

    class Meta:
        model = PurchaseItem
        fields = ['purchase_item_id', 'purchase', 'item', 'item_details', 'quantity']

class ProcurementItemSerializer(serializers.ModelSerializer):
    item_details = ItemSerializer(source='item', read_only=True)

    class Meta:
        model = ProcurementItem
        fields = ['procurement_item_id', 'procurement', 'item', 'item_details', 'requested_quantity']

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True, read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)

    class Meta:
        model = Purchase
        fields = ['purchase_id', 'purchase_date', 'supplier', 'total_cost', 'status', 
                'created_by', 'created_by_details', 'items']

class ProcurementSerializer(serializers.ModelSerializer):
    items = ProcurementItemSerializer(many=True, read_only=True)
    requested_by_details = UserSerializer(source='requested_by', read_only=True)
    approved_by_details = UserSerializer(source='approved_by', read_only=True)

    class Meta:
        model = Procurement
        fields = ['procurement_id', 'request_date', 'required_by', 'description', 'status', 
                'requested_by', 'requested_by_details', 
                'approved_by', 'approved_by_details', 'items']
