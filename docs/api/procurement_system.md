# Procurement System API Documentation

## Endpoints

### Suppliers

#### List Suppliers
- **URL**: `/api/procurement/suppliers/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "supplier_id": integer,
            "supplier_name": string,
            "contact_name": string,
            "phone": string,
            "email": string,
            "address": string
        }
    ]
}
```

#### Create Supplier
- **URL**: `/api/procurement/suppliers/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "supplier_name": string,
    "contact_name": string,
    "phone": string,
    "email": string,
    "address": string
}
```

### Purchases

#### List Purchases
- **URL**: `/api/procurement/purchases/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "purchase_id": integer,
            "supplier": integer,
            "purchase_date": date,
            "status": string,
            "total_amount": decimal,
            "items": [
                {
                    "item_id": integer,
                    "quantity": integer,
                    "unit_price": decimal
                }
            ]
        }
    ]
}
```

#### Create Purchase
- **URL**: `/api/procurement/purchases/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "supplier": integer,
    "purchase_date": date,
    "status": string,
    "total_amount": decimal,
    "items": [
        {
            "item": integer,
            "quantity": integer,
            "unit_price": decimal
        }
    ]
}
```

### Procurement Requests

#### List Procurement Requests
- **URL**: `/api/procurement/procurement-requests/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "request_id": integer,
            "requester": integer,
            "request_date": date,
            "status": string,
            "items": [
                {
                    "item_id": integer,
                    "quantity": integer,
                    "urgency": string
                }
            ]
        }
    ]
}
```

#### Create Procurement Request
- **URL**: `/api/procurement/procurement-requests/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Request Body**:
```json
{
    "items": [
        {
            "item": integer,
            "quantity": integer,
            "urgency": string
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
