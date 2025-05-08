from typing import List, Optional
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone
from .models import Transfer, TransferItem, Return, ShipmentTracking, ShipmentItem
from inventory_management.models import Item, Inventory
from inventory_management.services import InventoryService

class ShipmentService:
    @staticmethod
    @transaction.atomic
    def create_shipment(
        supplier_id: int,
        items: List[dict],
        shipment_date: str,
        estimated_arrival: str,
        tracking_number: str
    ) -> ShipmentTracking:
        """Create a new shipment with multiple items."""
        shipment = ShipmentTracking.objects.create(
            supplier_id=supplier_id,
            shipment_date=shipment_date,
            estimated_arrival=estimated_arrival,
            tracking_number=tracking_number,
            status='in_transit'
        )
        
        for item in items:
            ShipmentItem.objects.create(
                shipment=shipment,
                item_id=item['item_id'],
                quantity=item['quantity']
            )
            
        return shipment

    @staticmethod
    @transaction.atomic
    def update_shipment_status(
        shipment_id: int,
        new_status: str,
        warehouse_id: Optional[int] = None
    ) -> None:
        """Update shipment status and handle inventory updates if delivered."""
        shipment = ShipmentTracking.objects.select_for_update().get(
            shipment_id=shipment_id
        )
        
        if shipment.status == new_status:
            return
            
        if new_status == 'delivered' and warehouse_id:
            # Update inventory for all items in the shipment
            for shipment_item in shipment.shipmentitem_set.all():
                InventoryService.update_inventory(
                    item_id=shipment_item.item_id,
                    warehouse_id=warehouse_id,
                    quantity_change=shipment_item.quantity,
                    user_id=None  # TODO: Add user_id parameter
                )
                
        shipment.status = new_status
        shipment.save()

    @staticmethod
    @transaction.atomic
    def create_transfer(
        origin_warehouse_id: int,
        destination_warehouse_id: int,
        items: List[dict],
        requested_by_id: int,
        approved_by_id: int
    ) -> Transfer:
        """Create a new transfer between warehouses."""
        transfer = Transfer.objects.create(
            origin_warehouse_id=origin_warehouse_id,
            destination_warehouse_id=destination_warehouse_id,
            transfer_date=timezone.now(),
            requested_by_id=requested_by_id,
            approved_by_id=approved_by_id,
            status='pending'
        )
        
        for item in items:
            TransferItem.objects.create(
                transfer=transfer,
                item_id=item['item_id'],
                quantity=item['quantity']
            )
            
        return transfer

    @staticmethod
    @transaction.atomic
    def process_transfer(transfer_id: int) -> None:
        """Process a transfer by updating inventory in both warehouses."""
        transfer = Transfer.objects.select_for_update().get(
            transfer_id=transfer_id
        )
        
        if transfer.status != 'pending':
            raise ValueError("Transfer is not in pending status")
            
        for transfer_item in transfer.transferitem_set.all():
            # Decrease inventory in origin warehouse
            InventoryService.update_inventory(
                item_id=transfer_item.item_id,
                warehouse_id=transfer.origin_warehouse_id,
                quantity_change=-transfer_item.quantity,
                user_id=transfer.approved_by_id
            )
            
            # Increase inventory in destination warehouse
            InventoryService.update_inventory(
                item_id=transfer_item.item_id,
                warehouse_id=transfer.destination_warehouse_id,
                quantity_change=transfer_item.quantity,
                user_id=transfer.approved_by_id
            )
            
        transfer.status = 'completed'
        transfer.save()

    @staticmethod
    @transaction.atomic
    def create_return(
        item_id: int,
        return_quantity: int,
        reason: str,
        origin_transaction_id: int,
        approved_by_id: Optional[int],
        return_type: str
    ) -> Return:
        """Create a new return record."""
        return Return.objects.create(
            return_date=timezone.now(),
            reason=reason,
            origin_transaction_id=origin_transaction_id,
            return_quantity=return_quantity,
            status='pending',
            approved_by_id=approved_by_id,
            return_type=return_type,
            item_id=item_id
        )

    @staticmethod
    def get_active_shipments() -> List[dict]:
        """Get all active shipments with their items."""
        active_shipments = ShipmentTracking.objects.filter(
            status__in=['in_transit', 'processing']
        ).select_related('supplier')
        
        return [
            {
                'shipment_id': shipment.shipment_id,
                'tracking_number': shipment.tracking_number,
                'supplier_name': shipment.supplier.supplier_name,
                'status': shipment.status,
                'estimated_arrival': shipment.estimated_arrival,
                'items': [
                    {
                        'item_id': item.item.item_id,
                        'item_name': item.item.name,
                        'quantity': item.quantity
                    }
                    for item in shipment.shipmentitem_set.select_related('item').all()
                ]
            }
            for shipment in active_shipments
        ]

    @staticmethod
    def get_pending_transfers() -> List[dict]:
        """Get all pending transfers with their items."""
        pending_transfers = Transfer.objects.filter(
            status='pending'
        ).select_related(
            'origin_warehouse',
            'destination_warehouse',
            'requested_by'
        )
        
        return [
            {
                'transfer_id': transfer.transfer_id,
                'origin_warehouse': transfer.origin_warehouse.warehouse_name,
                'destination_warehouse': transfer.destination_warehouse.warehouse_name,
                'requested_by': transfer.requested_by.username,
                'transfer_date': transfer.transfer_date,
                'items': [
                    {
                        'item_id': item.item.item_id,
                        'item_name': item.item.name,
                        'quantity': item.quantity
                    }
                    for item in transfer.transferitem_set.select_related('item').all()
                ]
            }
            for transfer in pending_transfers
        ]
