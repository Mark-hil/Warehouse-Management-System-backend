from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Item, Inventory, InventoryAudit, Warehouse, Distribution, DistributionItem
from .serializers import CategorySerializer, ItemSerializer, InventorySerializer, InventoryAuditSerializer, WarehouseSerializer, DistributionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # Get warehouse IDs from request
            warehouse_ids = request.data.get('warehouses', [])
            
            # Create category first
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            category = serializer.save()

            # Add category to selected warehouses
            if warehouse_ids:
                warehouses = Warehouse.objects.filter(warehouse_id__in=warehouse_ids)
                for warehouse in warehouses:
                    WarehouseCategory.objects.create(
                        warehouse=warehouse,
                        category=category
                    )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"Error creating category: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        warehouse_id = request.query_params.get('warehouse')
        
        if warehouse_id:
            try:
                queryset = queryset.filter(warehouse_id=warehouse_id)
            except ValueError:
                return Response(
                    {"error": "Invalid warehouse ID format"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print('Received data:', request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print('Validation errors:', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        print('Update received data:', request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            print('Update validation errors:', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('Deleting item:', kwargs.get('pk'))
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def inventory_status(self, request, pk=None):
        item = self.get_object()
        inventory = Inventory.objects.filter(item=item)
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class DistributionViewSet(viewsets.ModelViewSet):
    queryset = Distribution.objects.all().order_by('-created_at')
    serializer_class = DistributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        distribution = serializer.save(created_by=self.request.user)
        items_data = self.request.data.get('items', [])
        
        for item_data in items_data:
            DistributionItem.objects.create(
                distribution=distribution,
                item_id=item_data['item'],
                quantity=item_data['quantity']
            )
            
            try:
                # Update source warehouse inventory
                source_inventory = Inventory.objects.get(
                    warehouse=distribution.source_warehouse,
                    item_id=item_data['item']
                )
                if source_inventory.available_quantity < item_data['quantity']:
                    raise serializers.ValidationError(f"Not enough quantity available in source warehouse for item {item_data['item']}")
                
                source_inventory.available_quantity -= item_data['quantity']
                source_inventory.save()
                
                # Create or update destination warehouse inventory
                dest_inventory, created = Inventory.objects.get_or_create(
                    warehouse=distribution.destination_warehouse,
                    item_id=item_data['item'],
                    defaults={'available_quantity': 0, 'minimum_quantity': 0}
                )
                dest_inventory.available_quantity += item_data['quantity']
                dest_inventory.save()
            except Inventory.DoesNotExist:
                raise serializers.ValidationError(f"Item {item_data['item']} not found in source warehouse inventory")

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            warehouse_id = request.query_params.get('warehouse')
            category_id = request.query_params.get('category')
            
            # Base queryset with select_related to avoid N+1 queries
            queryset = self.get_queryset().select_related('item', 'warehouse', 'item__category')
            
            if warehouse_id:
                try:
                    warehouse_id = int(warehouse_id)
                except ValueError:
                    return Response(
                        {"error": "Invalid warehouse ID format"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                # Check if warehouse exists
                try:
                    warehouse = Warehouse.objects.get(warehouse_id=warehouse_id)
                except Warehouse.DoesNotExist:
                    return Response(
                        {"error": "Warehouse not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                    
                # Filter by warehouse
                queryset = queryset.filter(warehouse=warehouse)
                
                # Handle category filter if present
                if category_id:
                    try:
                        category_id = int(category_id)
                    except ValueError:
                        return Response(
                            {"error": "Invalid category ID format"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                        
                    if not warehouse.categories.filter(category_id=category_id).exists():
                        return Response(
                            {"error": "This warehouse does not handle items from this category"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    queryset = queryset.filter(item__category_id=category_id)
                
            # Serialize and return the data
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            import traceback
            print(f'Error in inventory list: {str(e)}')
            print('Traceback:', traceback.format_exc())
            return Response(
                {"error": "An error occurred while fetching inventory. Please try again."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InventoryAuditViewSet(viewsets.ModelViewSet):
    queryset = InventoryAudit.objects.all()
    serializer_class = InventoryAuditSerializer
    permission_classes = [permissions.IsAuthenticated]
