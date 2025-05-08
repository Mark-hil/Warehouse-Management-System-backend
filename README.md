# Warehouse Management System API

A comprehensive Django REST API for managing warehouse operations, including inventory, procurement, shipment tracking, and reporting.

## Table of Contents
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Models](#models)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install django djangorestframework django-cors-headers
```

3. Apply migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### User Management (`/api/users/`)
- `/users/` - User CRUD operations
  - GET: List all users
  - POST: Create new user
  - PUT/PATCH: Update user
  - DELETE: Delete user
- `/permissions/` - Permission management
- `/notifications/` - User notifications

### Inventory Management (`/api/inventory/`)
- `/categories/` - Product categories
- `/items/` - Product items
  - Additional endpoint: `/items/{id}/inventory_status/`
- `/inventory/` - Inventory levels
- `/audit/` - Inventory audit logs

### Procurement System (`/api/procurement/`)
- `/suppliers/` - Supplier management
- `/purchases/` - Purchase orders
  - Additional endpoint: `/purchases/{id}/items/`
- `/purchase-items/` - Purchase order items
- `/procurement-requests/` - Procurement requests
  - Additional endpoint: `/procurement-requests/{id}/items/`
- `/procurement-items/` - Procurement request items

### Shipment Tracking (`/api/shipment/`)
- `/transfers/` - Internal transfers
  - Additional endpoint: `/transfers/{id}/items/`
- `/transfer-items/` - Transfer items
- `/returns/` - Return management
- `/shipments/` - Shipment tracking
  - Additional endpoint: `/shipments/{id}/items/`
- `/shipment-items/` - Shipment items

### Report Management (`/api/reports/`)
- `/reports/` - General reports
- `/maintenance/` - Maintenance history

## Authentication

The API uses Django REST Framework's authentication system. All endpoints require authentication.

### Authentication Methods
- Session Authentication (for browser access)
- Basic Authentication (for API access)

### Making Authenticated Requests

Using curl:
```bash
curl -H "Authorization: Basic $(echo -n 'username:password' | base64)" http://localhost:8000/api/endpoint/
```

Using the browser:
1. Navigate to any endpoint
2. Log in using the provided form
3. Session will be maintained for subsequent requests

## Models

### User Accounts
- User
  - username (string)
  - email (email)
  - password (string)
  - role (string)
  - assigned_branch (string)

### Inventory Management
- Category
  - name (string)
  - description (text)
- Item
  - name (string)
  - description (text)
  - category (foreign key)
  - unit_price (decimal)
  - current_quantity (integer)
  - reorder_level (integer)

### Procurement System
- Supplier
  - supplier_name (string)
  - contact_name (string)
  - phone (string)
  - email (email)
  - address (text)
- Purchase
  - supplier (foreign key)
  - purchase_date (date)
  - status (string)
  - total_amount (decimal)

### Shipment Tracking
- Transfer
  - origin_branch (string)
  - destination_branch (string)
  - transfer_date (date)
  - status (string)
- ShipmentTracking
  - supplier (foreign key)
  - shipment_date (date)
  - estimated_arrival (date)
  - tracking_number (string)
  - status (string)

### Report Management
- ReportItem
  - item (foreign key)
  - report_type (string)
  - report_date (date)
  - description (text)
- MaintenanceHistory
  - item (foreign key)
  - maintenance_date (date)
  - performed_by (string)
  - remarks (text)

## API Examples

### Authentication

```bash
# Get authentication token
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "password123"}' http://localhost:8000/api/token/

# Use token in subsequent requests
curl -H "Authorization: Token <your-token>" http://localhost:8000/api/endpoint/
```

### Inventory Management

```bash
# Create an item
curl -X POST -H "Authorization: Token <your-token>" -H "Content-Type: application/json" \
-d '{
    "name": "Laptop",
    "description": "High-end workstation",
    "unit": "piece",
    "unit_price": 1299.99
}' \
http://localhost:8000/api/inventory/items/

# Get inventory status
curl -H "Authorization: Token <your-token>" http://localhost:8000/api/inventory/items/1/inventory_status/
```

### Procurement System

```bash
# Create a procurement request
curl -X POST -H "Authorization: Token <your-token>" -H "Content-Type: application/json" \
-d '{
    "request_date": "2025-05-01",
    "required_by": "2025-05-30",
    "requested_by": 1,
    "status": "pending"
}' \
http://localhost:8000/api/procurement/procurement/

# Add items to procurement
curl -X POST -H "Authorization: Token <your-token>" -H "Content-Type: application/json" \
-d '{
    "procurement": 1,
    "item": 1,
    "requested_quantity": 5
}' \
http://localhost:8000/api/procurement/procurement-items/
```

### Shipment Tracking

```bash
# Create a transfer
curl -X POST -H "Authorization: Token <your-token>" -H "Content-Type: application/json" \
-d '{
    "origin_warehouse": 1,
    "destination_warehouse": 2,
    "transfer_date": "2025-05-01",
    "requested_by": 1,
    "approved_by": 1,
    "status": "pending"
}' \
http://localhost:8000/api/shipment/transfers/

# Track shipment
curl -X POST -H "Authorization: Token <your-token>" -H "Content-Type: application/json" \
-d '{
    "supplier": 1,
    "shipment_date": "2025-05-01",
    "estimated_arrival": "2025-05-05",
    "tracking_number": "SHIP123456",
    "status": "in_transit"
}' \
http://localhost:8000/api/shipment/shipments/
```

### Report Management

```bash
# Create a report
curl -X POST -H "Authorization: Token <your-token>" -H "Content-Type: application/json" \
-d '{
    "item": 1,
    "report_type": "damage",
    "report_date": "2025-05-01",
    "description": "Screen flickering issue",
    "reported_by": 1
}' \
http://localhost:8000/api/reports/reports/

# Add maintenance record
curl -X POST -H "Authorization: Token <your-token>" -H "Content-Type: application/json" \
-d '{
    "item": 1,
    "maintenance_date": "2025-05-01",
    "performed_by": "John Smith",
    "remarks": "Replaced screen panel"
}' \
http://localhost:8000/api/reports/maintenance/
```

## Response Formats

All endpoints return JSON responses in the following formats:

### Success Response
```json
{
    "id": 1,
    "field1": "value1",
    "field2": "value2",
    "created_at": "2025-05-01T10:00:00Z",
    "updated_at": "2025-05-01T10:00:00Z"
}
```

### List Response
```json
[
    {
        "id": 1,
        "field1": "value1",
        "field2": "value2"
    },
    {
        "id": 2,
        "field1": "value3",
        "field2": "value4"
    }
]
```

### Error Response
```json
{
    "error": "Error message",
    "code": "ERROR_CODE",
    "details": {
        "field": [
            "Error detail"
        ]
    }
}
```

## Status Codes

- 200: OK - Request succeeded
- 201: Created - Resource created successfully
- 204: No Content - Request succeeded (no response body)
- 400: Bad Request - Invalid request format or parameters
- 401: Unauthorized - Authentication required
- 403: Forbidden - Authenticated but not authorized
- 404: Not Found - Resource not found
- 409: Conflict - Resource conflict
- 500: Internal Server Error - Server error
