from django.contrib.auth import get_user_model
from inventory_management.models import Category, Item, Warehouse

# Create categories
categories = [
    {"name": "Electronics", "description": "Electronic devices and components"},
    {"name": "Office Supplies", "description": "General office supplies"},
    {"name": "Furniture", "description": "Office furniture and fixtures"},
]

# Create warehouses
warehouses = [
    {"warehouse_name": "Main Warehouse", "location": "123 Main St", "capacity": 1000},
    {"warehouse_name": "South Branch", "location": "456 South Ave", "capacity": 500},
]

# Create items
items = [
    {
        "name": "Laptop",
        "description": "High-performance business laptop",
        "unit_price": 999.99,
        "unit_measurement": "pcs",
        "category": "Electronics",
        "quantity": 50,
    },
    {
        "name": "Office Chair",
        "description": "Ergonomic office chair",
        "unit_price": 199.99,
        "unit_measurement": "pcs",
        "category": "Furniture",
        "quantity": 30,
    },
    {
        "name": "Printer Paper",
        "description": "A4 printer paper, 500 sheets",
        "unit_price": 4.99,
        "unit_measurement": "box",
        "category": "Office Supplies",
        "quantity": 200,
    },
    {
        "name": "Monitor",
        "description": "27-inch 4K monitor",
        "unit_price": 349.99,
        "unit_measurement": "pcs",
        "category": "Electronics",
        "quantity": 25,
    },
]

def create_test_data():
    # Create categories
    category_objects = {}
    for cat_data in categories:
        category = Category.objects.create(
            name=cat_data["name"],
            description=cat_data["description"]
        )
        category_objects[cat_data["name"]] = category
        print(f"Created category: {category.name}")

    # Create warehouses
    for wh_data in warehouses:
        warehouse = Warehouse.objects.create(
            warehouse_name=wh_data["warehouse_name"],
            location=wh_data["location"],
            capacity=wh_data["capacity"]
        )
        print(f"Created warehouse: {warehouse.name}")

    # Create items
    for item_data in items:
        category = category_objects[item_data["category"]]
        item = Item.objects.create(
            name=item_data["name"],
            description=item_data["description"],
            unit_price=item_data["unit_price"],
            unit_measurement=item_data["unit_measurement"],
            category=category,
            quantity=item_data["quantity"]
        )
        print(f"Created item: {item.name}")

if __name__ == "__main__":
    import os
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.backend.settings")
    django.setup()
    create_test_data()
