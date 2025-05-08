from inventory_management.models import Category, Item

# Create categories
categories = [
    {
        'name': 'Electronics',
        'description': 'Electronic devices and accessories'
    },
    {
        'name': 'Office Supplies',
        'description': 'General office supplies and stationery'
    },
    {
        'name': 'Furniture',
        'description': 'Office furniture and fixtures'
    }
]

# Create categories and store their IDs
category_map = {}
for cat_data in categories:
    category = Category.objects.create(
        name=cat_data['name'],
        description=cat_data['description']
    )
    category_map[cat_data['name']] = category
    print(f"Created category: {category.name}")

# Map items to categories
item_categories = {
    'Laptop': 'Electronics',
    'Monitor': 'Electronics',
    'Office Chair': 'Furniture',
    'Printer Paper': 'Office Supplies'
}

# Update items with categories
for item in Item.objects.all():
    if item.name in item_categories:
        category_name = item_categories[item.name]
        category = category_map[category_name]
        item.category = category
        item.save()
        print(f"Updated {item.name} with category {category.name}")

print("\nAll Items with Categories:")
for item in Item.objects.all():
    category_name = item.category.name if item.category else 'No Category'
    print(f"Name: {item.name}, Category: {category_name}")
