# Shipment Tracking API Documentation

## Endpoints

### Transfers

#### List Transfers
- **URL**: `/api/shipment/transfers/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "transfer_id": integer,
            "origin_branch": string,
            "destination_branch": string,
            "transfer_date": date,
            "status": string,
            "items": [
                {
                    "item_id": integer,
                    "quantity": integer
                }
            ]
        }
    ]
}
```

#### Create Transfer
- **URL**: `/api/shipment/transfers/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "origin_branch": string,
    "destination_branch": string,
    "transfer_date": date,
    "items": [
        {
            "item": integer,
            "quantity": integer
        }
    ]
}
```

### Returns

#### List Returns
- **URL**: `/api/shipment/returns/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "return_id": integer,
            "purchase": integer,
            "return_date": date,
            "reason": string,
            "status": string
        }
    ]
}
```

#### Create Return
- **URL**: `/api/shipment/returns/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "purchase": integer,
    "return_date": date,
    "reason": string
}
```

### Shipments

#### List Shipments
- **URL**: `/api/shipment/shipments/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "shipment_id": integer,
            "supplier": integer,
            "shipment_date": date,
            "estimated_arrival": date,
            "tracking_number": string,
            "status": string,
            "items": [
                {
                    "item_id": integer,
                    "quantity": integer
                }
            ]
        }
    ]
}
```

#### Create Shipment
- **URL**: `/api/shipment/shipments/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "supplier": integer,
    "shipment_date": date,
    "estimated_arrival": date,
    "tracking_number": string,
    "items": [
        {
            "item": integer,
            "quantity": integer
        }
    ]
}
```

#### Update Shipment Status
- **URL**: `/api/shipment/shipments/{id}/update_status/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "status": string
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
