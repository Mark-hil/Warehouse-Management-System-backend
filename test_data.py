from inventory_management.models import Category, Item, Warehouse, Inventory

# Create categories
categories = [
    Category(name="Electronics", description="Electronic devices and components"),
    Category(name="Office Supplies", description="General office supplies"),
    Category(name="Furniture", description="Office furniture and fixtures"),
]

Category.objects.bulk_create(categories)

# Create warehouses
warehouses = [
    Warehouse(warehouse_name="Main Warehouse", location="123 Main St", capacity=1000),
    Warehouse(warehouse_name="South Branch", location="456 South Ave", capacity=500),
]

Warehouse.objects.bulk_create(warehouses)

# Create items
items = [
    Item(
        name="Laptop",
        description="High-performance business laptop",
        unit="pcs",
        unit_price=999.99,
    ),
    Item(
        name="Office Chair",
        description="Ergonomic office chair",
        unit="pcs",
        unit_price=199.99,
    ),
    Item(
        name="Printer Paper",
        description="A4 printer paper, 500 sheets",
        unit="box",
        unit_price=4.99,
    ),
    Item(
        name="Monitor",
        description="27-inch 4K monitor",
        unit="pcs",
        unit_price=349.99,
    ),
]

Item.objects.bulk_create(items)

# Create inventory entries
main_warehouse = Warehouse.objects.get(warehouse_name="Main Warehouse")
items = Item.objects.all()

inventory_entries = [
    Inventory(
        item=item,
        warehouse=main_warehouse,
        available_quantity=50,
        minimum_quantity=10
    ) for item in items
]

Inventory.objects.bulk_create(inventory_entries)
print("Test data created successfully!")
