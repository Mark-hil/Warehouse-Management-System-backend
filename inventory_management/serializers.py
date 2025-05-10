from rest_framework import serializers
from .models import Category, Item, Inventory, InventoryAudit, Warehouse, Distribution, DistributionItem

class CategorySerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    def get_item_count(self, obj):
        return obj.items.count()

    class Meta:
        model = Category
        fields = ['category_id', 'name', 'description', 'created_at', 'item_count']

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
    current_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Warehouse
        fields = ['warehouse_id', 'warehouse_name', 'location', 'capacity', 'current_capacity', 'is_active', 'created_at', 'updated_at']

class DistributionItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = DistributionItem
        fields = ['distribution_item_id', 'item', 'item_name', 'quantity']

class DistributionSerializer(serializers.ModelSerializer):
    items = DistributionItemSerializer(many=True, read_only=True)
    source_warehouse_name = serializers.CharField(source='source_warehouse.warehouse_name', read_only=True)
    destination_warehouse_name = serializers.CharField(source='destination_warehouse.warehouse_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Distribution
        fields = ['distribution_id', 'source_warehouse', 'source_warehouse_name', 
                'destination_warehouse', 'destination_warehouse_name', 'created_by', 
                'created_by_name', 'created_at', 'estimated_delivery', 'status', 'items']

class InventorySerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ['inventory_id', 'warehouse', 'item', 'available_quantity', 'minimum_quantity']

class InventoryAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAudit
        fields = '__all__'
