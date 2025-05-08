from decimal import Decimal
from typing import List, Optional
from django.db import transaction
from django.db.models import F, Sum
from .models import Item, Inventory, InventoryAudit, Distribution, Warehouse
from user_accounts.models import User

class InventoryService:
    @staticmethod
    def get_item_inventory_status(item_id: int) -> dict:
        """Get detailed inventory status for an item across all warehouses."""
        inventory_items = Inventory.objects.filter(item_id=item_id).select_related('warehouse')
        total_quantity = sum(inv.available_quantity for inv in inventory_items)
        low_stock = any(inv.available_quantity <= inv.minimum_quantity for inv in inventory_items)
        
        return {
            'total_quantity': total_quantity,
            'low_stock': low_stock,
            'warehouse_stock': [
                {
                    'warehouse_id': inv.warehouse.warehouse_id,
                    'warehouse_name': inv.warehouse.warehouse_name,
                    'quantity': inv.available_quantity,
                    'minimum_quantity': inv.minimum_quantity
                }
                for inv in inventory_items
            ]
        }

    @staticmethod
    @transaction.atomic
    def update_inventory(item_id: int, warehouse_id: int, quantity_change: int, user_id: int) -> None:
        """Update inventory quantity and create audit record."""
        inventory = Inventory.objects.select_for_update().get(
            item_id=item_id,
            warehouse_id=warehouse_id
        )
        
        new_quantity = inventory.available_quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Insufficient inventory")
            
        inventory.available_quantity = new_quantity
        inventory.save()

        InventoryAudit.objects.create(
            inventory=inventory,
            audit_date=timezone.now(),
            audited_by_id=user_id,
            remarks=f"Quantity changed by {quantity_change}"
        )

    @staticmethod
    @transaction.atomic
    def create_distribution(
        item_id: int,
        warehouse_id: int,
        quantity: int,
        distributed_to_id: int,
        distributed_by_id: int
    ) -> Distribution:
        """Create a new distribution record and update inventory."""
        inventory = Inventory.objects.select_for_update().get(
            item_id=item_id,
            warehouse_id=warehouse_id
        )
        
        if inventory.available_quantity < quantity:
            raise ValueError("Insufficient inventory for distribution")
            
        distribution = Distribution.objects.create(
            item_id=item_id,
            warehouse_id=warehouse_id,
            distributed_to_id=distributed_to_id,
            distributed_by_id=distributed_by_id,
            distribution_date=timezone.now(),
            quantity=quantity,
            status='pending'
        )
        
        inventory.available_quantity -= quantity
        inventory.save()
        
        return distribution

    @staticmethod
    def get_low_stock_items() -> List[dict]:
        """Get all items that are below their minimum quantity."""
        low_stock_items = Inventory.objects.filter(
            available_quantity__lte=F('minimum_quantity')
        ).select_related('item', 'warehouse')
        
        return [
            {
                'item_id': inv.item.item_id,
                'item_name': inv.item.name,
                'warehouse_id': inv.warehouse.warehouse_id,
                'warehouse_name': inv.warehouse.warehouse_name,
                'available_quantity': inv.available_quantity,
                'minimum_quantity': inv.minimum_quantity
            }
            for inv in low_stock_items
        ]

    @staticmethod
    def get_warehouse_capacity_status(warehouse_id: int) -> dict:
        """Get the current capacity status of a warehouse."""
        warehouse = Warehouse.objects.get(warehouse_id=warehouse_id)
        total_items = Inventory.objects.filter(
            warehouse_id=warehouse_id
        ).aggregate(total=Sum('available_quantity'))['total'] or 0
        
        return {
            'warehouse_id': warehouse.warehouse_id,
            'warehouse_name': warehouse.warehouse_name,
            'total_capacity': warehouse.capacity,
            'used_capacity': total_items,
            'available_capacity': warehouse.capacity - total_items,
            'utilization_percentage': (total_items / warehouse.capacity) * 100 if warehouse.capacity > 0 else 0
        }
