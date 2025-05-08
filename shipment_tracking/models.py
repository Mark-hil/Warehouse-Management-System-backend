from django.db import models
from user_accounts.models import User
from inventory_management.models import Item, Warehouse
from procurement_system.models import Supplier

class Transfer(models.Model):
    transfer_id = models.AutoField(primary_key=True)
    origin_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='origin_warehouse', null=True)
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='destination_warehouse', null=True)
    transfer_date = models.DateField()
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfer_requested_by')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfer_approved_by')
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'transfers'

class TransferItem(models.Model):
    transfer_item_id = models.AutoField(primary_key=True)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'transfer_items'

class Return(models.Model):
    return_id = models.AutoField(primary_key=True)
    return_date = models.DateField()
    reason = models.TextField()
    origin_transaction_id = models.IntegerField()
    return_quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    return_type = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        db_table = 'returns'

class ShipmentTracking(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    shipment_date = models.DateField()
    estimated_arrival = models.DateField()
    tracking_number = models.CharField(max_length=255)
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'shipment_tracking'

class ShipmentItem(models.Model):
    shipment_item_id = models.AutoField(primary_key=True)
    shipment = models.ForeignKey(ShipmentTracking, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'shipment_items'
