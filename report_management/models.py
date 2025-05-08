from django.db import models
from inventory_management.models import Item
from user_accounts.models import User

class ReportItem(models.Model):
    report_item_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=255)
    report_date = models.DateField()
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'report_items'

class MaintenanceHistory(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    performed_by = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'maintenance_history'
