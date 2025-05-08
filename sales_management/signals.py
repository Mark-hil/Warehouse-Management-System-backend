from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from .models import Sale, SaleItem, Payment
from inventory_management.models import Inventory

@receiver(post_save, sender=SaleItem)
def update_sale_total(sender, instance, created, **kwargs):
    """Update the sale total amount when a sale item is added or modified."""
    if created or instance.pk:
        with transaction.atomic():
            sale = instance.sale
            total = sum(item.total_price for item in sale.saleitem_set.all())
            Sale.objects.filter(pk=sale.pk).update(total_amount=total)

@receiver(pre_save, sender=SaleItem)
def calculate_total_price(sender, instance, **kwargs):
    """Calculate the total price for a sale item before saving."""
    instance.total_price = (instance.unit_price * instance.quantity) - instance.discount

@receiver(post_save, sender=SaleItem)
def update_inventory(sender, instance, created, **kwargs):
    """Update inventory quantities when a sale is made."""
    if created:
        with transaction.atomic():
            inventory = Inventory.objects.select_for_update().get(item=instance.item)
            if inventory.available_quantity >= instance.quantity:
                inventory.available_quantity -= instance.quantity
                inventory.save()
            else:
                raise ValueError("Insufficient inventory quantity")

@receiver(post_save, sender=Payment)
def update_sale_status(sender, instance, created, **kwargs):
    """Update sale status when payment is received."""
    if created or instance.status == 'COMPLETED':
        with transaction.atomic():
            sale = instance.sale
            total_paid = sum(
                payment.amount 
                for payment in Payment.objects.filter(
                    sale=sale, 
                    status='COMPLETED'
                )
            )
            
            if total_paid >= sale.total_amount:
                sale.status = 'PAID'
            elif total_paid > 0:
                sale.status = 'PARTIALLY_PAID'
            else:
                sale.status = 'UNPAID'
            
            sale.save()
