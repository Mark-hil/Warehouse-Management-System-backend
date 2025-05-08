from decimal import Decimal
from typing import List, Optional
from django.db import transaction
from django.db.models import F, Sum
from django.utils import timezone
from .models import Supplier, Purchase, PurchaseItem, Procurement, ProcurementItem
from inventory_management.models import Item, Inventory
from inventory_management.services import InventoryService

class ProcurementService:
    @staticmethod
    @transaction.atomic
    def create_procurement_request(
        items: List[dict],
        requested_by_id: int,
        required_by: str
    ) -> Procurement:
        """Create a new procurement request with multiple items."""
        procurement = Procurement.objects.create(
            request_date=timezone.now(),
            required_by=required_by,
            requested_by_id=requested_by_id,
            status='pending'
        )
        
        for item in items:
            ProcurementItem.objects.create(
                procurement=procurement,
                item_id=item['item_id'],
                requested_quantity=item['quantity']
            )
            
        return procurement

    @staticmethod
    @transaction.atomic
    def approve_procurement(procurement_id: int, approved_by_id: int) -> None:
        """Approve a procurement request and create purchase orders if needed."""
        procurement = Procurement.objects.select_for_update().get(
            procurement_id=procurement_id
        )
        
        if procurement.status != 'pending':
            raise ValueError("Procurement request is not in pending status")
            
        procurement.status = 'approved'
        procurement.approved_by_id = approved_by_id
        procurement.save()

    @staticmethod
    @transaction.atomic
    def create_purchase_order(
        supplier_id: int,
        items: List[dict],
        purchase_date: str
    ) -> Purchase:
        """Create a new purchase order with multiple items."""
        total_amount = sum(
            Decimal(str(item['unit_price'])) * item['quantity']
            for item in items
        )
        
        purchase = Purchase.objects.create(
            supplier_id=supplier_id,
            purchase_date=purchase_date,
            status='pending',
            total_amount=total_amount
        )
        
        for item in items:
            PurchaseItem.objects.create(
                purchase=purchase,
                item_id=item['item_id'],
                ordered_quantity=item['quantity'],
                received_quantity=0,
                unit_price=item['unit_price']
            )
            
        return purchase

    @staticmethod
    @transaction.atomic
    def receive_purchase_items(
        purchase_id: int,
        received_items: List[dict],
        warehouse_id: int
    ) -> None:
        """Record received items from a purchase order and update inventory."""
        purchase = Purchase.objects.select_for_update().get(
            purchase_id=purchase_id
        )
        
        if purchase.status == 'completed':
            raise ValueError("Purchase order is already completed")
            
        for item in received_items:
            purchase_item = PurchaseItem.objects.select_for_update().get(
                purchase_id=purchase_id,
                item_id=item['item_id']
            )
            
            if purchase_item.received_quantity + item['quantity'] > purchase_item.ordered_quantity:
                raise ValueError(f"Received quantity exceeds ordered quantity for item {item['item_id']}")
                
            purchase_item.received_quantity += item['quantity']
            purchase_item.save()
            
            # Update inventory
            InventoryService.update_inventory(
                item_id=item['item_id'],
                warehouse_id=warehouse_id,
                quantity_change=item['quantity'],
                user_id=item['received_by']
            )
            
        # Check if all items are received
        all_items_received = all(
            item.received_quantity == item.ordered_quantity
            for item in purchase.purchaseitem_set.all()
        )
        
        if all_items_received:
            purchase.status = 'completed'
            purchase.save()

    @staticmethod
    def get_pending_procurements() -> List[dict]:
        """Get all pending procurement requests with their items."""
        procurements = Procurement.objects.filter(
            status='pending'
        ).select_related('requested_by')
        
        return [
            {
                'procurement_id': proc.procurement_id,
                'request_date': proc.request_date,
                'required_by': proc.required_by,
                'requested_by': proc.requested_by.username,
                'items': [
                    {
                        'item_id': item.item.item_id,
                        'item_name': item.item.name,
                        'requested_quantity': item.requested_quantity
                    }
                    for item in proc.procurementitem_set.select_related('item').all()
                ]
            }
            for proc in procurements
        ]

    @staticmethod
    def get_supplier_performance(supplier_id: int) -> dict:
        """Get performance metrics for a supplier."""
        purchases = Purchase.objects.filter(supplier_id=supplier_id)
        total_purchases = purchases.count()
        completed_on_time = purchases.filter(status='completed').count()
        
        return {
            'total_purchases': total_purchases,
            'completed_on_time': completed_on_time,
            'completion_rate': (completed_on_time / total_purchases * 100) if total_purchases > 0 else 0,
            'average_delivery_time': 0  # TODO: Implement delivery time tracking
        }
