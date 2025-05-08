from django.db import models
from user_accounts.models import User

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categories'

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=50, default='unit')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')

    class Meta:
        db_table = 'items'

class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()

    class Meta:
        db_table = 'warehouses'

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    available_quantity = models.IntegerField()
    minimum_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'inventory'

class InventoryAudit(models.Model):
    audit_id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    audit_date = models.DateField()
    audited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inventory_audit'

class Distribution(models.Model):
    distribution_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    distributed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='distribution_received')
    distributed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='distribution_made')
    distribution_date = models.DateField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'distributions'
