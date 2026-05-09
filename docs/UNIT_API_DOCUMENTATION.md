# Unit API Documentation

## Overview

The Unit API provides endpoints for managing measurement units in the Cash Flow Management system. This is a master data API that manages different types of measurement units (pieces, square meters, grams, etc.) used throughout the application for standardizing measurements.

## Base URL
```
/api/v1/common/units
```

## Authentication
All unit endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Get All Units

### Endpoint
```
GET /api/v1/common/units
```

### Description
Retrieves a paginated list of all measurement units available in the system. This is a master data endpoint that returns predefined measurement units for use in other parts of the application.

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
curl -X GET "http://localhost:5000/api/v1/common/units?page=1&limit=10" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json"
```

### Response Format

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Units retrieved successfully",
  "data": [
    {
      "id": 1,
      "code": "PIECE",
      "name": "Cái",
      "is_deleted": false,
      "created_at": "2026-05-09T09:30:00Z",
      "updated_at": "2026-05-09T09:30:00Z",
      "created_by_user_id": 1,
      "updated_by_user_id": 1
    },
    {
      "id": 2,
      "code": "M2",
      "name": "m²",
      "is_deleted": false,
      "created_at": "2026-05-09T09:35:00Z",
      "updated_at": "2026-05-09T09:35:00Z",
      "created_by_user_id": 1,
      "updated_by_user_id": 1
    },
    {
      "id": 3,
      "code": "GRAM",
      "name": "Gram",
      "is_deleted": false,
      "created_at": "2026-05-09T09:40:00Z",
      "updated_at": "2026-05-09T09:40:00Z",
      "created_by_user_id": 1,
      "updated_by_user_id": 1
    },
    {
      "id": 4,
      "code": "KG",
      "name": "Kilogram",
      "is_deleted": false,
      "created_at": "2026-05-09T09:45:00Z",
      "updated_at": "2026-05-09T09:45:00Z",
      "created_by_user_id": 1,
      "updated_by_user_id": 1
    },
    {
      "id": 5,
      "code": "LITER",
      "name": "Lít",
      "is_deleted": false,
      "created_at": "2026-05-09T09:50:00Z",
      "updated_at": "2026-05-09T09:50:00Z",
      "created_by_user_id": 1,
      "updated_by_user_id": 1
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

---

## Create Unit

### Endpoint
```
POST /api/v1/common/units
```

### Description
Creates a new measurement unit in the system. This is typically used by administrators to add new measurement types.

### Request Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | string | Yes | Unique unit code (max 50 chars) |
| name | string | Yes | Unit display name (max 255 chars) |

### Request Example
```bash
curl -X POST "http://localhost:5000/api/v1/common/units" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "code": "METER",
    "name": "Mét"
  }'
```

### Response Format

#### Success Response (201 Created)
```json
{
  "status": "success",
  "message": "Unit created successfully",
  "data": {
    "id": 6,
    "code": "METER",
    "name": "Mét",
    "is_deleted": false,
    "created_at": "2026-05-09T10:00:00Z",
    "updated_at": "2026-05-09T10:00:00Z",
    "created_by_user_id": 123,
    "updated_by_user_id": 123
  }
}
```

#### Error Responses

**400 Bad Request**
```json
{
  "status": "error",
  "message": "code is required"
}
```

**401 Unauthorized**
```json
{
  "status": "error",
  "message": "Access token is required or invalid"
}
```

---

## Get Unit by ID

### Endpoint
```
GET /api/v1/common/units/{unit_id}
```

### Description
Retrieves a specific measurement unit by its ID.

### Request Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| unit_id | integer | Yes | ID of the unit to retrieve |

### Request Example
```bash
curl -X GET "http://localhost:5000/api/v1/common/units/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json"
```

### Response Format

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Unit retrieved successfully",
  "data": {
    "id": 1,
    "code": "PIECE",
    "name": "Cái",
    "is_deleted": false,
    "created_at": "2026-05-09T09:30:00Z",
    "updated_at": "2026-05-09T09:30:00Z",
    "created_by_user_id": 1,
    "updated_by_user_id": 1
  }
}
```

#### Error Responses

**404 Not Found**
```json
{
  "status": "error",
  "message": "Unit not found"
}
```

**401 Unauthorized**
```json
{
  "status": "error",
  "message": "Access token is required or invalid"
}
```

---

## Update Unit

### Endpoint
```
PUT /api/v1/common/units/{unit_id}
```

### Description
Updates an existing measurement unit. Only provided fields will be updated.

### Request Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| unit_id | integer | Yes | ID of the unit to update |

### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | string | No | Updated unit code (max 50 chars) |
| name | string | No | Updated unit name (max 255 chars) |

### Request Example
```bash
curl -X PUT "http://localhost:5000/api/v1/common/units/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chiếc"
  }'
```

### Response Format

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Unit updated successfully",
  "data": {
    "id": 1,
    "code": "PIECE",
    "name": "Chiếc",
    "is_deleted": false,
    "created_at": "2026-05-09T09:30:00Z",
    "updated_at": "2026-05-09T10:05:00Z",
    "created_by_user_id": 1,
    "updated_by_user_id": 123
  }
}
```

#### Error Responses

**400 Bad Request**
```json
{
  "status": "error",
  "message": "code is required"
}
```

**404 Not Found**
```json
{
  "status": "error",
  "message": "Unit not found"
}
```

**401 Unauthorized**
```json
{
  "status": "error",
  "message": "Access token is required or invalid"
}
```

---

## Delete Unit

### Endpoint
```
DELETE /api/v1/common/units/{unit_id}
```

### Description
Soft deletes a measurement unit. The unit is marked as deleted but remains in the database for data integrity.

### Request Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| unit_id | integer | Yes | ID of the unit to delete |

### Request Example
```bash
curl -X DELETE "http://localhost:5000/api/v1/common/units/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json"
```

### Response Format

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Unit deleted successfully"
}
```

#### Error Responses

**404 Not Found**
```json
{
  "status": "error",
  "message": "Unit not found"
}
```

**401 Unauthorized**
```json
{
  "status": "error",
  "message": "Access token is required or invalid"
}
```

---

## Data Model

### Unit Object
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique unit identifier |
| code | string | Unique unit code (max 50 chars) |
| name | string | Unit display name (max 255 chars) |
| is_deleted | boolean | Soft delete flag |
| created_at | string | ISO 8601 timestamp |
| updated_at | string | ISO 8601 timestamp |
| created_by_user_id | integer | User who created the unit |
| updated_by_user_id | integer | User who last updated the unit |

### Common Unit Types

#### Standard Measurement Units
| Code | Name | Category | Usage Examples |
|------|------|----------|----------------|
| PIECE | Cái | Count | Individual items, products |
| M2 | m² | Area | Property, land, floor space |
| METER | Mét | Length | Height, width, distance |
| GRAM | Gram | Weight | Jewelry, small items |
| KG | Kilogram | Weight | Food, bulk items |
| LITER | Lít | Volume | Liquids, fuels |
| ML | Mililít | Volume | Medicine, cosmetics |
| BOX | Hộp | Packaging | Packaged goods |
| BOTTLE | Chai | Packaging | Beverages, liquids |
| BAG | Túi | Packaging | Groceries, items |
| SET | Bộ | Grouping | Tool sets, collections |
| PAIR | Cặp | Grouping | Shoes, gloves, socks |
| DOZEN | Tá | Grouping | Eggs, items sold by dozen |

#### Specialized Units
| Code | Name | Category | Usage Examples |
|------|------|----------|----------------|
| SQFT | Feet vuông | Area | Real estate (US/UK) |
| ACRE | Mẫu | Area | Land, agriculture |
| OUNCE | Ounce | Weight | Precious metals |
| TROY_OUNCE | Ounce troy | Weight | Gold, silver |
| CARAT | Carat | Weight | Diamonds, gems |
| GALLON | Galon | Volume | Fuel (US) |
| IMP_GALLON | Galon Anh | Volume | Fuel (UK) |
| TON | Tấn | Weight | Heavy materials |
| METRIC_TON | Tấn metric | Weight | International standard |

### Unit Categories

#### By Measurement Type
- **Count**: PIECE, BOX, BOTTLE, BAG, SET, PAIR, DOZEN
- **Area**: M2, SQFT, ACRE, HECTARE
- **Length**: METER, CENTIMETER, INCH, FOOT, YARD
- **Weight**: GRAM, KG, OUNCE, TROY_OUNCE, CARAT, TON
- **Volume**: LITER, ML, GALLON, IMP_GALLON, CUBIC_METER

#### By Application Domain
- **General**: PIECE, BOX, BAG, SET
- **Real Estate**: M2, SQFT, ACRE, HECTARE
- **Jewelry**: GRAM, OUNCE, TROY_OUNCE, CARAT
- **Food**: KG, GRAM, LITER, ML
- **Industrial**: TON, METRIC_TON, CUBIC_METER
- **Retail**: DOZEN, PAIR, SET

### Pagination

The API supports pagination using `page` and `limit` parameters:

- **page**: Page number (starts from 1)
- **limit**: Number of items per page (default: 10, max: 100)

**Example with pagination:**
```bash
GET /api/v1/common/units?page=2&limit=5
```

### Implementation Details

#### Controller Logic
```python
def list_units(self):
    params = self._get_pagination_params()  # Extract page/limit
    items = self.unit_service.get_all(page=params['page'], limit=params['limit'])
    data = [i.to_dict() for i in items]
    return self.ok(data=data)

def create_unit(self):
    data = request.get_json(force=True)
    if not data:
        raise BadRequestException('Request body is required')
    UnitReq(data)  # Validate required fields
    user_id = get_current_user_id()
    entity = ComUnit(
        code=data.get('code'),
        name=data.get('name'),
        created_by_user_id=user_id,
        updated_by_user_id=user_id
    )
    created = self.unit_service.create(entity)
    return self.created(data=created.to_dict())
```

#### Service Method
```python
def get_all(self, page: int = 1, limit: int = 10) -> List[ComUnit]:
    return self.repository.find_all(page, limit)
```

### Security Features

1. **JWT Authentication**: Required for all unit operations
2. **Master Data Protection**: Only authorized users can modify units
3. **Soft Delete**: Units are soft deleted, not permanently removed
4. **Audit Trail**: Created/updated timestamps and user tracking
5. **Data Integrity**: Referential integrity with other entities

### Usage Examples

#### JavaScript/TypeScript
```javascript
async function getUnits(page = 1, limit = 10) {
  const token = localStorage.getItem('access_token');
  
  try {
    const response = await fetch(
      `/api/v1/common/units?page=${page}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch units');
    }
    
    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Error fetching units:', error);
    throw error;
  }
}

// Usage
const units = await getUnits(1, 10);
console.log('Available units:', units);

// Create new unit
async function createUnit(unitData) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('/api/v1/common/units', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(unitData)
  });
  
  return response.json();
}

const newUnit = await createUnit({
  code: 'METER',
  name: 'Mét'
});
```

#### Python
```python
import requests

def get_units(access_token, page=1, limit=10):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    params = {'page': page, 'limit': limit}
    
    response = requests.get(
        'http://localhost:5000/api/v1/common/units',
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        response.raise_for_status()

def create_unit(access_token, unit_data):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        'http://localhost:5000/api/v1/common/units',
        headers=headers,
        json=unit_data
    )
    
    return response.json()

# Usage
units = get_units('your_access_token_here')
print(units)

new_unit = create_unit('your_access_token_here', {
    'code': 'METER',
    'name': 'Mét'
})
print(new_unit)
```

### Common Use Cases

1. **Transaction Forms**: Populate unit dropdowns in transaction creation
2. **Product Management**: Define measurement units for products
3. **Inventory Tracking**: Track quantities with appropriate units
4. **Reporting**: Display quantities with proper units
5. **Conversion**: Convert between different units
6. **Localization**: Display appropriate units for different regions

### Integration with Other APIs

The Unit API integrates with:

- **Asset API**: Assets reference units for measurement
- **Transaction API**: Transactions use units for quantities
- **Product API**: Products have associated units
- **Report API**: Reports display quantities with units

### Error Handling Best Practices

1. **Network Errors**: Implement retry logic for failed requests
2. **Authentication**: Handle 401 errors by refreshing tokens
3. **Validation**: Display meaningful error messages for validation failures
4. **Not Found**: Handle 404 errors gracefully
5. **Pagination**: Implement pagination controls for large datasets

### Testing

#### Unit Test Example
```python
def test_get_units():
    # Mock authentication
    with patch('modules.common_master.routes.jwt_required_custom'):
        # Mock service
        with patch.object(controller.unit_service, 'get_all') as mock_service:
            mock_unit = ComUnit()
            mock_unit.id = 1
            mock_unit.code = "PIECE"
            mock_unit.name = "Cái"
            mock_service.return_value = [mock_unit]
            
            # Test the endpoint
            response = client.get('/api/v1/common/units', headers={
                'Authorization': 'Bearer test_token'
            })
            
            assert response.status_code == 200
            data = response.get_json()
            assert len(data['data']) == 1
            assert data['data'][0]['code'] == "PIECE"

def test_create_unit():
    # Mock authentication
    with patch('modules.common_master.routes.jwt_required_custom'):
        # Mock service
        with patch.object(controller.unit_service, 'create') as mock_service:
            mock_unit = ComUnit()
            mock_unit.id = 1
            mock_unit.code = "METER"
            mock_unit.name = "Mét"
            mock_service.return_value = mock_unit
            
            # Test the endpoint
            response = client.post('/api/v1/common/units', 
                headers={'Authorization': 'Bearer test_token'},
                json={'code': 'METER', 'name': 'Mét'}
            )
            
            assert response.status_code == 201
            data = response.get_json()
            assert data['data']['code'] == "METER"
```

### Performance Considerations

1. **Database Indexing**: Ensure `code` field is indexed for unique lookups
2. **Caching**: Implement caching for units (master data changes infrequently)
3. **Pagination Limits**: Implement reasonable page size limits
4. **Query Optimization**: Use efficient database queries

### Data Seeding

Units are typically seeded during database initialization:

```sql
INSERT INTO com_unit (code, name) VALUES
('PIECE', 'Cái'),
('M2', 'm²'),
('METER', 'Mét'),
('GRAM', 'Gram'),
('KG', 'Kilogram'),
('LITER', 'Lít'),
('ML', 'Mililít'),
('BOX', 'Hộp'),
('BOTTLE', 'Chai'),
('BAG', 'Túi'),
('SET', 'Bộ'),
('PAIR', 'Cặp'),
('DOZEN', 'Tá');
```

### Related Endpoints

- `GET /api/v1/common/units` - List all units
- `POST /api/v1/common/units` - Create new unit
- `GET /api/v1/common/units/{id}` - Get specific unit
- `PUT /api/v1/common/units/{id}` - Update unit
- `DELETE /api/v1/common/units/{id}` - Delete unit

---

## Quick Reference

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/units` | List all units | Yes |
| POST | `/units` | Create unit | Yes |
| GET | `/units/{id}` | Get unit details | Yes |
| PUT | `/units/{id}` | Update unit | Yes |
| DELETE | `/units/{id}` | Delete unit | Yes |

## Master Data vs User Data

**Important**: Units are master data (system-wide) rather than user-specific data. All users see the same list of units, unlike wallets which are user-specific.

For more information about other master data endpoints, see the complete API documentation.
