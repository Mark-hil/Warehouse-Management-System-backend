# User Accounts API Documentation

## Endpoints

### Users

#### List Users
- **URL**: `/api/users/users/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Admin or Staff
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "id": integer,
            "username": string,
            "email": string,
            "role": string,
            "assigned_branch": string,
            "date_joined": datetime
        }
    ]
}
```

#### Create User
- **URL**: `/api/users/users/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Admin
- **Request Body**:
```json
{
    "username": string,
    "email": string,
    "password": string,
    "role": string,
    "assigned_branch": string
}
```

#### Update User
- **URL**: `/api/users/users/{id}/`
- **Method**: PUT/PATCH
- **Auth required**: Yes
- **Permissions**: Admin or Self
- **Request Body**: Same as Create User

#### Delete User
- **URL**: `/api/users/users/{id}/`
- **Method**: DELETE
- **Auth required**: Yes
- **Permissions**: Admin

### Permissions

#### List Permissions
- **URL**: `/api/users/permissions/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Admin
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "id": integer,
            "name": string,
            "codename": string
        }
    ]
}
```

### Notifications

#### List Notifications
- **URL**: `/api/users/notifications/`
- **Method**: GET
- **Auth required**: Yes
- **Permissions**: Self
- **Response**:
```json
{
    "count": integer,
    "results": [
        {
            "id": integer,
            "user": integer,
            "message": string,
            "created_at": datetime,
            "read": boolean
        }
    ]
}
```

#### Mark Notification as Read
- **URL**: `/api/users/notifications/{id}/mark_read/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: Self

## Error Responses

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
