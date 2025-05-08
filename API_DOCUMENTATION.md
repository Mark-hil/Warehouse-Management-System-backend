# API Documentation

## Authentication

All API endpoints require authentication. To access the API endpoints, you need to:

1. Obtain an authentication token by making a POST request to:
```
POST /api/token/
```
Request body:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

2. Include the token in all subsequent requests using the Authorization header:
```
Authorization: Token your_token_here
```

## API Endpoints

### User Management
- `POST /api/users/users/` - Create a new user
- `GET /api/users/users/` - List all users
- `GET /api/users/users/{id}/` - Get user details
- `PUT /api/users/users/{id}/` - Update user
- `DELETE /api/users/users/{id}/` - Delete user

- `GET /api/users/permissions/` - List permissions
- `POST /api/users/permissions/` - Create permission
- `GET /api/users/permissions/{id}/` - Get permission details

- `GET /api/users/notifications/` - List notifications
- `POST /api/users/notifications/` - Create notification
- `GET /api/users/notifications/{id}/` - Get notification details

### Inventory Management
- `GET /api/inventory/categories/` - List all categories
- `POST /api/inventory/categories/` - Create category

- `GET /api/inventory/items/` - List all items
- `POST /api/inventory/items/` - Create item
- `GET /api/inventory/items/{id}/` - Get item details
- `GET /api/inventory/items/{id}/inventory_status/` - Get item inventory status

- `GET /api/inventory/inventory/` - List inventory
- `POST /api/inventory/inventory/` - Create inventory record

- `GET /api/inventory/audit/` - List audit records
- `POST /api/inventory/audit/` - Create audit record

### Procurement System
- `GET /api/procurement/suppliers/` - List all suppliers
- `POST /api/procurement/suppliers/` - Create supplier

- `GET /api/procurement/purchases/` - List all purchases
- `POST /api/procurement/purchases/` - Create purchase
- `GET /api/procurement/purchases/{id}/` - Get purchase details
- `GET /api/procurement/purchases/{id}/items/` - Get purchase items

- `GET /api/procurement/purchase-items/` - List purchase items
- `POST /api/procurement/purchase-items/` - Create purchase item

- `GET /api/procurement/procurement/` - List procurement requests
- `POST /api/procurement/procurement/` - Create procurement request
- `GET /api/procurement/procurement/{id}/items/` - Get procurement items

- `GET /api/procurement/procurement-items/` - List procurement items
- `POST /api/procurement/procurement-items/` - Create procurement item

### Shipment Tracking
- `GET /api/shipment/transfers/` - List all transfers
- `POST /api/shipment/transfers/` - Create transfer
- `GET /api/shipment/transfers/{id}/` - Get transfer details
- `GET /api/shipment/transfers/{id}/items/` - Get transfer items

- `GET /api/shipment/transfer-items/` - List transfer items
- `POST /api/shipment/transfer-items/` - Create transfer item

- `GET /api/shipment/returns/` - List all returns
- `POST /api/shipment/returns/` - Create return

- `GET /api/shipment/shipments/` - List all shipments
- `POST /api/shipment/shipments/` - Create shipment
- `GET /api/shipment/shipments/{id}/items/` - Get shipment items

- `GET /api/shipment/shipment-items/` - List shipment items
- `POST /api/shipment/shipment-items/` - Create shipment item

### Report Management
- `GET /api/reports/` - List all reports
- `POST /api/reports/` - Create report
- `GET /api/reports/{id}/` - Get report details
- `PUT /api/reports/{id}/` - Update report
- `DELETE /api/reports/{id}/` - Delete report

## Request/Response Examples

### Authentication
```
POST /api/token/
Request:
{
    "username": "admin",
    "password": "admin123"
}

Response:
{
    "token": "your_auth_token_here"
}
```

### Create Item
```
POST /api/inventory/items/
Headers:
Authorization: Token your_token_here
Content-Type: application/json

Request:
{
    "name": "Test Item",
    "description": "This is a test item",
    "unit": "piece",
    "unit_price": "10.99"
}

Response:
{
    "id": 1,
    "name": "Test Item",
    "description": "This is a test item",
    "unit": "piece",
    "unit_price": "10.99"
}
```

### Create Purchase
```
POST /api/procurement/purchases/
Headers:
Authorization: Token your_token_here
Content-Type: application/json

Request:
{
    "supplier": 1,
    "purchase_date": "2025-04-29",
    "status": "pending",
    "items": [
        {
            "item": 1,
            "quantity": 10,
            "unit_price": "10.99"
        }
    ]
}

Response:
{
    "id": 1,
    "supplier": 1,
    "purchase_date": "2025-04-29",
    "status": "pending",
    "items": [
        {
            "id": 1,
            "item": 1,
            "quantity": 10,
            "unit_price": "10.99"
        }
    ]
}
```

## Error Responses

### Authentication Error
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Permission Error
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### Not Found Error
```json
{
    "detail": "Not found."
}
```

### Validation Error
```json
{
    "field_name": [
        "Error message"
    ]
}
```
