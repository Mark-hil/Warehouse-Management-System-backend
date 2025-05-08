# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-05-01

### Added
- Initial release of the Warehouse Management System
- User authentication with token-based system
- Inventory Management System
  - Category management
  - Item management with inventory tracking
  - Warehouse management
  - Inventory audit logging
- Procurement System
  - Supplier management
  - Purchase order processing
  - Procurement request workflow
  - Item-level tracking for purchases
- Shipment Tracking System
  - Internal transfer management
  - Return processing
  - Shipment tracking with status updates
  - Item-level tracking for shipments
- Report Management System
  - Item condition reporting
  - Maintenance history tracking
  - Detailed item reports
- API Documentation
  - Comprehensive README
  - Detailed API documentation
  - Example requests and responses
  - Error handling documentation

### Features
- Token-based authentication for secure API access
- CRUD operations for all major entities
- Status tracking for procurement, shipments, and transfers
- Detailed reporting and maintenance history
- Inventory level monitoring
- Multi-warehouse support
- User role management
- Audit logging for inventory changes

### Technical Details
- Built with Django 5.0.1
- Django REST Framework for API endpoints
- Token authentication
- JSON response format
- Proper error handling
- Database migrations
- CORS support

### API Endpoints
- User Management (/api/users/)
- Inventory Management (/api/inventory/)
- Procurement System (/api/procurement/)
- Shipment Tracking (/api/shipment/)
- Report Management (/api/reports/)

### Security
- Token-based authentication
- Role-based access control
- Secure password handling
- Protected API endpoints

### Documentation
- Installation guide
- API documentation
- Usage examples
- Response format documentation
- Error handling guide
