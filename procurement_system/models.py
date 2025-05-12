from django.db import models
from django.utils import timezone
from user_accounts.models import User
from inventory_management.models import Item, Warehouse

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    zip_code = models.CharField(max_length=20, default='')
    country = models.CharField(max_length=100, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'suppliers'

class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    status = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'purchases'

class PurchaseItem(models.Model):
    purchase_item_id = models.AutoField(primary_key=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered_quantity = models.IntegerField()
    received_quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'purchase_items'

class Procurement(models.Model):
    procurement_id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    required_by = models.DateField()
    description = models.TextField(blank=True, null=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='procurement_requested_by')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='procurement_approved_by')
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'procurement'

class ProcurementItem(models.Model):
    procurement_item_id = models.AutoField(primary_key=True)
    procurement = models.ForeignKey(Procurement, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    requested_quantity = models.IntegerField()

    class Meta:
        db_table = 'procurement_items'
