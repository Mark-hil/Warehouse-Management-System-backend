# API Documentation

## Overview

This document provides comprehensive documentation for the Warehouse Management System API.

## Base URL
All API endpoints are relative to: `http://localhost:8000/api/`

## Quick Reference

### Core Endpoints
- User Management: `/api/users/`
- Inventory Management: `/api/inventory/`
- Procurement System: `/api/procurement/`
- Shipment Tracking: `/api/shipment/`
- Report Management: `/api/reports/`

### Common Operations
- List items: `GET /{endpoint}/`
- Get single item: `GET /{endpoint}/{id}/`
- Create item: `POST /{endpoint}/`
- Update item: `PUT/PATCH /{endpoint}/{id}/`
- Delete item: `DELETE /{endpoint}/{id}/`

## Authentication

The API uses token-based authentication. To obtain a token:

```bash
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "token": "your-auth-token"
}
```

Use this token in all subsequent requests:
```bash
Authorization: Token your-auth-token
```

## Inventory Management

### Categories

#### List Categories
```
GET /inventory/categories/
```

#### Create Category
```
POST /inventory/categories/
{
    "name": "Electronics",
    "description": "Electronic devices and accessories"
}
```

### Items

#### List Items
```
GET /inventory/items/
```

#### Create Item
```
POST /inventory/items/
{
    "name": "Laptop",
    "description": "High-end workstation",
    "unit": "piece",
    "unit_price": 1299.99
}
```

#### Get Item Inventory Status
```
GET /inventory/items/{id}/inventory_status/
```

## Procurement System

### Suppliers

#### List Suppliers
```
GET /procurement/suppliers/
```

#### Create Supplier
```
POST /procurement/suppliers/
{
    "supplier_name": "Tech Suppliers Inc",
    "contact_name": "John Doe",
    "phone": "+1-555-0123",
    "email": "john@techsuppliers.com",
    "address": "123 Tech Street"
}
```

### Procurement Requests

#### Create Procurement Request
```
POST /procurement/procurement/
{
    "request_date": "2025-05-01",
    "required_by": "2025-05-30",
    "requested_by": 1,
    "status": "pending"
}
```

#### Add Items to Procurement
```
POST /procurement/procurement-items/
{
    "procurement": 1,
    "item": 1,
    "requested_quantity": 5
}
```

#### Update Procurement Status
```
PATCH /procurement/procurement/{id}/
{
    "status": "approved",
    "approved_by": 1
}
```

### Purchases

#### Create Purchase Order
```
POST /procurement/purchases/
{
    "supplier": 1,
    "purchase_date": "2025-05-01",
    "status": "ordered",
    "total_amount": 15499.85
}
```

#### Add Items to Purchase
```
POST /procurement/purchase-items/
{
    "purchase": 1,
    "item": 1,
    "ordered_quantity": 10,
    "received_quantity": 0,
    "unit_price": 1299.99
}
```

## Shipment Tracking

### Transfers

#### Create Transfer
```
POST /shipment/transfers/
{
    "origin_warehouse": 1,
    "destination_warehouse": 2,
    "transfer_date": "2025-05-01",
    "requested_by": 1,
    "approved_by": 1,
    "status": "pending"
}
```

#### Add Transfer Items
```
POST /shipment/transfer-items/
{
    "transfer": 1,
    "item": 1,
    "quantity": 5
}
```

### Returns

#### Create Return
```
POST /shipment/returns/
{
    "return_date": "2025-05-01",
    "reason": "Defective item",
    "origin_transaction_id": 1,
    "return_quantity": 2,
    "status": "pending",
    "return_type": "supplier_return",
    "item": 1
}
```

### Shipment Tracking

#### Create Shipment
```
POST /shipment/shipments/
{
    "supplier": 1,
    "shipment_date": "2025-05-01",
    "estimated_arrival": "2025-05-05",
    "tracking_number": "SHIP123456",
    "status": "in_transit"
}
```

## Report Management

### Reports

#### Create Report
```
POST /reports/reports/
{
    "item": 1,
    "report_type": "damage",
    "report_date": "2025-05-01",
    "description": "Screen flickering issue",
    "reported_by": 1
}
```

#### List Reports
```
GET /reports/reports/
```

### Maintenance

#### Create Maintenance Record
```
POST /reports/maintenance/
{
    "item": 1,
    "maintenance_date": "2025-05-01",
    "performed_by": "John Smith",
    "remarks": "Replaced screen panel"
}
```

#### List Maintenance Records
```
GET /reports/maintenance/
```

## Status Codes and Error Handling

### Success Codes
- 200: OK - Request succeeded
- 201: Created - Resource created successfully
- 204: No Content - Request succeeded (no response body)

### Error Codes
- 400: Bad Request - Invalid request format or parameters
- 401: Unauthorized - Authentication required
- 403: Forbidden - Authenticated but not authorized
- 404: Not Found - Resource not found
- 409: Conflict - Resource conflict
- 500: Internal Server Error - Server error

### Error Response Format
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

## Pagination

List endpoints support pagination using the following query parameters:

- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10)

Example:
```
GET /api/inventory/items/?page=2&page_size=20
```

Response:
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/inventory/items/?page=3&page_size=20",
    "previous": "http://localhost:8000/api/inventory/items/?page=1&page_size=20",
    "results": [
        ...
    ]
}
```

## Filtering and Searching

Many endpoints support filtering and searching using query parameters:

### Examples

1. Filter by status:
```
GET /api/procurement/procurement/?status=pending
```

2. Search by name:
```
GET /api/inventory/items/?search=laptop
```

3. Filter by date range:
```
GET /api/reports/reports/?start_date=2025-05-01&end_date=2025-05-31
```

4. Filter by multiple fields:
```
GET /api/shipment/shipments/?status=in_transit&supplier=1
```
