from django.db import models
from django.utils import timezone
from user_accounts.models import User

from django.utils import timezone

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

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
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, through='WarehouseCategory', related_name='warehouses')

    @property
    def current_capacity(self):
        return self.inventory_set.aggregate(total=models.Sum('available_quantity'))['total'] or 0

    class Meta:
        db_table = 'warehouses'

class WarehouseCategory(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'warehouse_categories'
        unique_together = ('warehouse', 'category')

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    available_quantity = models.IntegerField()
    minimum_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'inventory'

class Distribution(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    distribution_id = models.AutoField(primary_key=True)
    source_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, related_name='source_distributions')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, related_name='destination_distributions')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_distributions')
    created_at = models.DateTimeField(default=timezone.now)
    estimated_delivery = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'distributions'

class DistributionItem(models.Model):
    distribution_item_id = models.AutoField(primary_key=True)
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'distribution_items'

class InventoryAudit(models.Model):
    audit_id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    audit_date = models.DateField()
    audited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inventory_audit'


