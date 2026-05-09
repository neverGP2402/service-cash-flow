# Cash Flow Management API Documentation

## Overview

Cash Flow Management System API provides endpoints for personal finance management, including user authentication, transaction management, asset tracking, and financial reporting.

**Base URL:** `http://localhost:5000`
**API Version:** `v1`
**Content-Type:** `application/json`

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Response Format

All API responses follow this format:

### Success Response
```json
{
    "status": "success|created",
    "message": "Operation completed successfully",
    "data": {
        // Response data
    },
    "timestamp": "2025-05-08T09:30:00.000Z"
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error description",
    "error_code": "ERROR_CODE",
    "timestamp": "2025-05-08T09:30:00.000Z"
}
```

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /api/v1/auth/register`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "Password123",
    "full_name": "John Doe",
    "birthday": "1990-01-15",
    "gender": "MALE",
    "address": "123 Main Street, District 1, Ho Chi Minh City",
    "avatar": "https://example.com/avatars/john.jpg",
    "province_id": 79,
    "ward_id": 12345,
    "role_permission_id": 2
}
```

**Required Fields:**
- `username` (string, 3-50 chars): Unique username
- `email` (string): Valid email address
- `password` (string, 8-255 chars): At least 1 uppercase, 1 lowercase, 1 digit

**Optional Fields:**
- `full_name` (string, max 255 chars): User's full name
- `birthday` (string): Date in YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY format
- `gender` (string): MALE, FEMALE, or OTHER
- `address` (string): User's address
- `avatar` (string): URL to profile image
- `province_id` (integer): Province ID
- `ward_id` (integer): Ward ID
- `role_permission_id` (integer): Role permission ID

**Response (201 Created):**
```json
{
    "status": "created",
    "message": "User registered successfully",
    "data": {
        "id": 1,
        "username": "john_doe",
        "email": "john.doe@example.com",
        "full_name": "John Doe",
        "birthday": "1990-01-15T00:00:00Z",
        "age": 35,
        "gender": "MALE",
        "address": "123 Main Street, District 1, Ho Chi Minh City",
        "avatar": "https://example.com/avatars/john.jpg",
        "province_id": 79,
        "ward_id": 12345,
        "status": "ACTIVE",
        "register_date": "2025-05-08T09:30:00Z",
        "created_at": "2025-05-08T09:30:00Z"
    }
}
```

**Error Responses:**
- `400 Bad Request`: Validation errors
- `409 Conflict`: Username or email already exists

---

### Login User

Authenticate user and receive tokens.

**Endpoint:** `POST /api/v1/auth/login`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "Password123",
    "device_info": "Postman Test",
    "ip_address": "127.0.0.1"
}
```

**Required Fields:**
- `username` (string): Username or email
- `password` (string): User password

**Optional Fields:**
- `device_info` (string): Device information
- `ip_address` (string): Client IP address

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Login successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john.doe@example.com",
            "full_name": "John Doe",
            "last_login_time": "2025-05-08T09:30:00Z"
        }
    }
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields
- `401 Unauthorized`: Invalid credentials

---

### Logout User

Invalidate user session.

**Endpoint:** `POST /api/v1/auth/logout`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Logout successful"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token

## Transaction Endpoints

### Create Transaction

Create a new financial transaction.

**Endpoint:** `POST /api/v1/transaction`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "type": "EXPENSE",
    "category_id": 1,
    "amount": 150000.50,
    "date": "2025-05-08T14:30:00Z",
    "description": "Lunch at restaurant",
    "formality_transaction": "BANK",
    "wallet_id": 1,
    "origin_transaction_id": 1,
    "bill_image": "https://example.com/bills/lunch.jpg"
}
```

**Required Fields:**
- `type` (string): INCOME or EXPENSE
- `amount` (number): Transaction amount
- `date` (string): ISO 8601 datetime

**Optional Fields:**
- `category_id` (integer): Transaction category
- `description` (string): Transaction description
- `formality_transaction` (string): CASH, BANK, or OTHER
- `wallet_id` (integer): Wallet ID
- `origin_transaction_id` (integer): Origin transaction ID
- `bill_image` (string): URL to bill image

**Response (201 Created):**
```json
{
    "status": "created",
    "message": "Transaction created successfully",
    "data": {
        "id": 1,
        "user_id": 1,
        "type": "EXPENSE",
        "category_id": 1,
        "amount": 150000.50,
        "date": "2025-05-08T14:30:00Z",
        "description": "Lunch at restaurant",
        "formality_transaction": "BANK",
        "wallet_id": 1,
        "origin_transaction_id": 1,
        "status": "COMPLETED",
        "created_at": "2025-05-08T14:30:00Z"
    }
}
```

---

### Get Transactions

Get user transactions with pagination and filtering.

**Endpoint:** `GET /api/v1/transaction`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (integer, default: 1): Page number
- `limit` (integer, default: 20): Items per page
- `type` (string): Filter by type (INCOME/EXPENSE)
- `category_id` (integer): Filter by category
- `start_date` (string): Filter by start date (YYYY-MM-DD)
- `end_date` (string): Filter by end date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Transactions retrieved successfully",
    "data": {
        "transactions": [
            {
                "id": 1,
                "type": "EXPENSE",
                "category_id": 1,
                "amount": 150000.50,
                "date": "2025-05-08T14:30:00Z",
                "description": "Lunch at restaurant",
                "status": "COMPLETED"
            }
        ],
        "pagination": {
            "page": 1,
            "limit": 20,
            "total": 1,
            "pages": 1
        }
    }
}
```

## Asset Endpoints

### Get User Assets

Get user's asset portfolio.

**Endpoint:** `GET /api/v1/asset`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Assets retrieved successfully",
    "data": {
        "assets": [
            {
                "id": 1,
                "asset_id": 1,
                "asset_name": "Gold",
                "amount": 2.5,
                "price": 11500000,
                "current_value": 28750000,
                "unit_name": "Chỉ",
                "transaction_date": "2025-01-15T00:00:00Z"
            }
        ],
        "total_value": 28750000
    }
}
```

---

### Create Asset

Add new asset to portfolio.

**Endpoint:** `POST /api/v1/asset`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "asset_id": 1,
    "wallet_id": 1,
    "amount": 1.0,
    "price": 11500000,
    "description": "Buy 1 chỉ gold",
    "unit_id": 1,
    "transaction_date": "2025-05-08T14:30:00Z"
}
```

**Response (201 Created):**
```json
{
    "status": "created",
    "message": "Asset created successfully",
    "data": {
        "id": 1,
        "asset_id": 1,
        "wallet_id": 1,
        "amount": 1.0,
        "price": 11500000,
        "current_value": 11500000,
        "description": "Buy 1 chỉ gold",
        "unit_id": 1,
        "transaction_date": "2025-05-08T14:30:00Z",
        "created_at": "2025-05-08T14:30:00Z"
    }
}
```

## Report Endpoints

### Get Monthly Report

Get monthly financial report.

**Endpoint:** `GET /api/v1/report/monthly`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `month` (integer, required): Month (1-12)
- `year` (integer, required): Year (e.g., 2025)

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Monthly report retrieved successfully",
    "data": {
        "month": 5,
        "year": 2025,
        "income": 15000000,
        "expense": 8500000,
        "net_income": 6500000,
        "transaction_count": 25,
        "categories": [
            {
                "category_id": 1,
                "category_name": "Food",
                "amount": 2500000,
                "percentage": 29.4
            }
        ]
    }
}
```

---

### Get Asset Summary

Get asset portfolio summary.

**Endpoint:** `GET /api/v1/report/assets`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Asset summary retrieved successfully",
    "data": {
        "total_value": 50000000,
        "assets_by_type": [
            {
                "asset_type": "Gold",
                "value": 28750000,
                "percentage": 57.5
            },
            {
                "asset_type": "Cash",
                "value": 21250000,
                "percentage": 42.5
            }
        ],
        "profit_loss": {
            "total_profit": 2500000,
            "profit_percentage": 5.2
        }
    }
}
```

## Configuration Endpoints

### Get Categories

Get transaction categories.

**Endpoint:** `GET /api/v1/common/categories`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `type` (string): Filter by type (INCOME/EXPENSE)

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Categories retrieved successfully",
    "data": [
        {
            "id": 1,
            "code": "FOOD",
            "name": "Food & Dining",
            "type": "EXPENSE"
        },
        {
            "id": 2,
            "code": "SALARY",
            "name": "Salary",
            "type": "INCOME"
        }
    ]
}
```

---

### Get Wallets

Get user's wallets.

**Endpoint:** `GET /api/v1/common/wallets`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Wallets retrieved successfully",
    "data": [
        {
            "id": 1,
            "code": "CASH",
            "name": "Tiền mặt",
            "type": "CASH",
            "balance": 5000000
        },
        {
            "id": 2,
            "code": "BANK_VCB",
            "name": "Vietcombank",
            "type": "BANK",
            "balance": 15000000
        }
    ]
}
```

## Error Codes

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `AUTHENTICATION_FAILED` | 401 | Invalid credentials or token |
| `AUTHORIZATION_FAILED` | 403 | Insufficient permissions |
| `RESOURCE_NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |

## Rate Limiting

API requests are limited to:
- 100 requests per minute per IP
- 1000 requests per hour per user

## SDK Examples

### JavaScript (Axios)

```javascript
// Login
const login = async (username, password) => {
    try {
        const response = await axios.post('/api/v1/auth/login', {
            username,
            password,
            device_info: 'Web App',
            ip_address: '127.0.0.1'
        });
        
        const { access_token, refresh_token } = response.data.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        
        return response.data;
    } catch (error) {
        console.error('Login failed:', error.response.data);
        throw error;
    }
};

// Create transaction
const createTransaction = async (transactionData) => {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await axios.post('/api/v1/transaction', transactionData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        return response.data;
    } catch (error) {
        console.error('Create transaction failed:', error.response.data);
        throw error;
    }
};
```

### Python (Requests)

```python
import requests

class CashFlowAPI:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
    
    def login(self, username, password):
        """Authenticate user"""
        response = requests.post(f'{self.base_url}/api/v1/auth/login', json={
            'username': username,
            'password': password,
            'device_info': 'Python Client',
            'ip_address': '127.0.0.1'
        })
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['data']['access_token']
            self.refresh_token = data['data']['refresh_token']
            return data
        else:
            raise Exception(f'Login failed: {response.json()}')
    
    def create_transaction(self, transaction_data):
        """Create new transaction"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f'{self.base_url}/api/v1/transaction',
            json=transaction_data,
            headers=headers
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f'Create transaction failed: {response.json()}')
    
    def get_transactions(self, page=1, limit=20, **filters):
        """Get user transactions"""
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'page': page, 'limit': limit, **filters}
        
        response = requests.get(
            f'{self.base_url}/api/v1/transaction',
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Get transactions failed: {response.json()}')

# Usage
api = CashFlowAPI()
api.login('john_doe', 'Password123')

# Create transaction
transaction = api.create_transaction({
    'type': 'EXPENSE',
    'amount': 150000.50,
    'description': 'Lunch',
    'date': '2025-05-08T14:30:00Z'
})

print(transaction)
```

## Support

For API support and questions:
- Email: support@cashflow.com
- Documentation: https://docs.cashflow.com
- GitHub: https://github.com/cashflow/api
