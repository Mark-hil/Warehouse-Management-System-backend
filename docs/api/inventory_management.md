# Inventory Management API Documentation

## Endpoints

### Categories

#### List Categories
- **URL**: `/api/inventory/categories/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "category_id": integer,
            "name": string,
            "description": string
        }
    ]
}
```

#### Create Category
- **URL**: `/api/inventory/categories/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "name": string,
    "description": string
}
```

### Items

#### List Items
- **URL**: `/api/inventory/items/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "item_id": integer,
            "name": string,
            "description": string,
            "category": integer,
            "unit_price": decimal,
            "current_quantity": integer,
            "reorder_level": integer,
            "created_at": datetime
        }
    ]
}
```

#### Create Item
- **URL**: `/api/inventory/items/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "name": string,
    "description": string,
    "category": integer,
    "unit_price": decimal,
    "current_quantity": integer,
    "reorder_level": integer
}
```

#### Get Item Inventory Status
- **URL**: `/api/inventory/items/{id}/inventory_status/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "item_id": integer,
    "name": string,
    "current_quantity": integer,
    "reorder_level": integer,
    "status": string,
    "last_updated": datetime
}
```

### Inventory

#### List Inventory
- **URL**: `/api/inventory/inventory/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "inventory_id": integer,
            "item": {
                "item_id": integer,
                "name": string
            },
            "branch_location": string,
            "available_quantity": integer
        }
    ]
}
```

### Audit

#### List Audit Logs
- **URL**: `/api/inventory/audit/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "audit_id": integer,
            "inventory": integer,
            "old_quantity": integer,
            "new_quantity": integer,
            "reason": string,
            "audited_by": integer,
            "audit_date": datetime
        }
    ]
}
```

## Error Responses

### 400 Bad Request
```json
{
    "field_name": [
        "Error message"
    ]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```
