# Report Management API Documentation

## Endpoints

### Reports

#### List Reports
- **URL**: `/api/reports/reports/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "report_id": integer,
            "item": {
                "item_id": integer,
                "name": string
            },
            "report_type": string,
            "report_date": date,
            "description": string
        }
    ]
}
```

#### Create Report
- **URL**: `/api/reports/reports/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "item": integer,
    "report_type": string,
    "description": string
}
```

### Maintenance History

#### List Maintenance Records
- **URL**: `/api/reports/maintenance/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "maintenance_id": integer,
            "item": {
                "item_id": integer,
                "name": string
            },
            "maintenance_date": date,
            "performed_by": string,
            "remarks": string
        }
    ]
}
```

#### Create Maintenance Record
- **URL**: `/api/reports/maintenance/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Request Body**:
```json
{
    "item": integer,
    "maintenance_date": date,
    "performed_by": string,
    "remarks": string
}
```

#### Get Item Maintenance History
- **URL**: `/api/reports/maintenance/item/{item_id}/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Any authenticated user
- **Response**:
```json
{
    "item": {
        "item_id": integer,
        "name": string
    },
    "maintenance_records": [
        {
            "maintenance_id": integer,
            "maintenance_date": date,
            "performed_by": string,
            "remarks": string
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
