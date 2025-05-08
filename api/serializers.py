from rest_framework import serializers

# Import models from their new locations
from inventory_management.models import (
    Item as ProductDim,
    Category as CategoryDim,
    Inventory as InventoryAndPriceFact
)
from user_accounts.models import User as CustomerDim
from procurement_system.models import (
    Supplier as SupplierDim,
    Purchase as SalesFact
)
from shipment_tracking.models import (
    ShipmentTracking as ShippingDim,
    Return as PaymentDim
)
from dimensions.models import DateDim, StoreDim, PromotionDim

class InventoryAndPriceFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAndPriceFact
        fields = '__all__'

class ProductDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDim
        fields = '__all__'

class DateDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateDim
        fields = '__all__'

class StoreDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDim
        fields = '__all__'

class SupplierDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierDim
        fields = '__all__'

class CategoryDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryDim
        fields = '__all__'

class SalesFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesFact
        fields = '__all__'

class CustomerDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDim
        fields = '__all__'

class PromotionDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionDim
        fields = '__all__'

class ShippingDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDim
        fields = '__all__'

class PaymentDimSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDim
        fields = '__all__'
