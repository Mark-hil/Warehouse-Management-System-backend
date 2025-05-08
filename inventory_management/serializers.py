from rest_framework import serializers
from .models import Category, Item, Inventory, InventoryAudit, Warehouse

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    unitPrice = serializers.DecimalField(source='unit_price', max_digits=12, decimal_places=2)
    unitMeasurement = serializers.CharField(source='unit', required=True)
    category = CategorySerializer(read_only=True)
    categoryId = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Item
        fields = ['item_id', 'name', 'description', 'unitPrice', 'unitMeasurement', 'category', 'categoryId']

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class InventoryAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAudit
        fields = '__all__'
