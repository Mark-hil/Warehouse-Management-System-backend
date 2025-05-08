from django.db import models
from django.utils import timezone
from user_accounts.models import User
from inventory_management.models import Item
from dimensions.models import StoreDim

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    customer_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers'

class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(StoreDim, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sales'

class SaleItem(models.Model):
    sale_item_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'sale_items'

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('MOBILE_PAYMENT', 'Mobile Payment'),
    ]

    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    payment_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=100, choices=PAYMENT_STATUS)
    reference_number = models.CharField(max_length=255, unique=True)
    transaction_details = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'payments'

class PriceHistory(models.Model):
    price_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'price_history'
        indexes = [
            models.Index(fields=['item', 'effective_from', 'effective_to']),
        ]

class Report(models.Model):
    REPORT_TYPES = [
        ('SALES', 'Sales Report'),
        ('INVENTORY', 'Inventory Report'),
        ('PROCUREMENT', 'Procurement Report'),
        ('CUSTOMER', 'Customer Report'),
        ('FINANCIAL', 'Financial Report'),
    ]

    report_id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=100, choices=REPORT_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    parameters = models.JSONField()
    result_data = models.JSONField()
    file_path = models.CharField(max_length=512, null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'reports'
        indexes = [
            models.Index(fields=['report_type', 'generated_at']),
        ]
