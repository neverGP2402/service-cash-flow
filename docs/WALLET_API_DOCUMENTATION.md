# Wallet API Documentation

## Overview

The Wallet API provides endpoints for managing user wallets in the Cash Flow Management system. Users can create, read, update, and delete their personal wallets.

## Base URL
```
/api/v1/common/wallets
```

## Authentication
All wallet endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Get User Wallets

### Endpoint
```
GET /api/v1/common/wallets
```

### Description
Retrieves a paginated list of wallets belonging to the authenticated user.

### Request Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Query Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number for pagination |
| limit | integer | No | 10 | Number of items per page |

### Request Example
```bash
curl -X GET "http://localhost:5000/api/v1/common/wallets?page=1&limit=10" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json"
```

### Response Format

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Wallets retrieved successfully",
  "data": [
    {
      "id": 1,
      "user_id": 123,
      "code": "WALLET001",
      "name": "Ví Tiền Mặt",
      "type": "CASH",
      "is_deleted": false,
      "created_at": "2026-05-09T09:30:00Z",
      "updated_at": "2026-05-09T09:30:00Z",
      "created_by_user_id": 123,
      "updated_by_user_id": 123
    },
    {
      "id": 2,
      "user_id": 123,
      "code": "BANK001",
      "name": "Vietcombank",
      "type": "BANK",
      "is_deleted": false,
      "created_at": "2026-05-09T09:35:00Z",
      "updated_at": "2026-05-09T09:35:00Z",
      "created_by_user_id": 123,
      "updated_by_user_id": 123
    }
  ]
}
```

#### Error Responses

**401 Unauthorized**
```json
{
  "status": "error",
  "message": "Access token is required or invalid"
}
```

**500 Internal Server Error**
```json
{
  "status": "error",
  "message": "Internal server error"
}
```

### Data Model

#### Wallet Object
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique wallet identifier |
| user_id | integer | ID of the wallet owner |
| code | string | Unique wallet code (max 50 chars) |
| name | string | Wallet display name (max 255 chars) |
| type | string | Wallet type (CASH, BANK, CREDIT_CARD, etc.) |
| is_deleted | boolean | Soft delete flag |
| created_at | string | ISO 8601 timestamp |
| updated_at | string | ISO 8601 timestamp |
| created_by_user_id | integer | User who created the wallet |
| updated_by_user_id | integer | User who last updated the wallet |

### Wallet Types
| Type | Description |
|------|-------------|
| CASH | Tiền mặt |
| BANK | Tài khoản ngân hàng |
| CREDIT_CARD | Thẻ tín dụng |
| DEBIT_CARD | Thẻ ghi nợ |
| E_WALLET | Ví điện tử (Momo, ZaloPay, etc.) |
| INVESTMENT | Tài khoản đầu tư |
| OTHER | Loại khác |

### Pagination

The API supports pagination using `page` and `limit` parameters:

- **page**: Page number (starts from 1)
- **limit**: Number of items per page (default: 10, max: 100)

**Example with pagination:**
```bash
GET /api/v1/common/wallets?page=2&limit=5
```

### Implementation Details

#### Controller Logic
```python
def list_wallets(self):
    user_id = get_current_user_id()  # Get authenticated user ID
    params = self._get_pagination_params()  # Extract page/limit
    items = self.wallet_service.get_by_user_id(user_id, params['page'], params['limit'])
    data = [i.to_dict() for i in items]
    return self.ok(data=data)
```

#### Service Method
```python
def get_by_user_id(self, user_id: int, page: int = 1, limit: int = 10) -> List[ComWallet]:
    return self.repository.find_by_user_id(user_id, page, limit)
```

### Security Features

1. **User Isolation**: Users can only access their own wallets
2. **JWT Authentication**: Required for all wallet operations
3. **Soft Delete**: Wallets are soft deleted, not permanently removed
4. **Audit Trail**: Created/updated timestamps and user tracking

### Usage Examples

#### JavaScript/TypeScript
```javascript
async function getUserWallets(page = 1, limit = 10) {
  const token = localStorage.getItem('access_token');
  
  try {
    const response = await fetch(
      `/api/v1/common/wallets?page=${page}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch wallets');
    }
    
    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Error fetching wallets:', error);
    throw error;
  }
}

// Usage
const wallets = await getUserWallets(1, 10);
console.log('User wallets:', wallets);
```

#### Python
```python
import requests

def get_user_wallets(access_token, page=1, limit=10):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    params = {'page': page, 'limit': limit}
    
    response = requests.get(
        'http://localhost:5000/api/v1/common/wallets',
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        response.raise_for_status()

# Usage
wallets = get_user_wallets('your_access_token_here')
print(wallets)
```

### Common Use Cases

1. **Dashboard Display**: Show user's wallet list on main dashboard
2. **Transaction Forms**: Populate wallet selection dropdowns
3. **Financial Reports**: Include wallet information in reports
4. **Budget Management**: Track spending per wallet
5. **Account Reconciliation**: Match wallet balances

### Error Handling Best Practices

1. **Network Errors**: Implement retry logic for failed requests
2. **Authentication**: Handle 401 errors by refreshing tokens or redirecting to login
3. **Empty Results**: Handle cases where user has no wallets
4. **Pagination**: Implement infinite scroll or pagination controls
5. **Rate Limiting**: Respect API rate limits

### Testing

#### Unit Test Example
```python
def test_get_user_wallets():
    # Mock authentication
    with patch('modules.common_master.routes.get_current_user_id') as mock_user:
        mock_user.return_value = 123
        
        # Mock service
        with patch.object(controller.wallet_service, 'get_by_user_id') as mock_service:
            mock_wallet = ComWallet()
            mock_wallet.id = 1
            mock_wallet.user_id = 123
            mock_wallet.name = "Test Wallet"
            mock_service.return_value = [mock_wallet]
            
            # Test the endpoint
            response = client.get('/api/v1/common/wallets', headers={
                'Authorization': 'Bearer test_token'
            })
            
            assert response.status_code == 200
            data = response.get_json()
            assert len(data['data']) == 1
            assert data['data'][0]['name'] == "Test Wallet"
```

### Performance Considerations

1. **Database Indexing**: Ensure `user_id` field is indexed
2. **Pagination Limits**: Implement reasonable page size limits
3. **Caching**: Consider caching frequently accessed wallet data
4. **Query Optimization**: Use efficient database queries

### Related Endpoints

- `POST /api/v1/common/wallets` - Create new wallet
- `GET /api/v1/common/wallets/{id}` - Get specific wallet
- `PUT /api/v1/common/wallets/{id}` - Update wallet
- `DELETE /api/v1/common/wallets/{id}` - Delete wallet

---

## Quick Reference

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/wallets` | List user wallets | Yes |
| POST | `/wallets` | Create wallet | Yes |
| GET | `/wallets/{id}` | Get wallet details | Yes |
| PUT | `/wallets/{id}` | Update wallet | Yes |
| DELETE | `/wallets/{id}` | Delete wallet | Yes |

For more information about other wallet operations, see the complete API documentation.
