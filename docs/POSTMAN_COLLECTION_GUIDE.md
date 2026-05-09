# Postman Collection Guide

## Quick Start

1. **Import Collection**
   - Open Postman
   - Click `Import` → `File`
   - Select `postman_enhanced_collection.json`
   - Collection will appear as "Cash Flow Management API - Enhanced"

2. **Set Environment Variables**
   - Go to `Environments` tab
   - Create new environment or use existing
   - Add variable: `baseUrl` = `http://localhost:5000`

3. **Test Authentication Flow**
   - Run "Register User (Full)" request
   - Run "Login User" request (tokens auto-saved)
   - Run "Logout User" request

## Request Examples

### 1. Register User (Full Profile)

```http
POST http://localhost:5000/api/v1/auth/register
Content-Type: application/json

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

### 2. Register User (Minimal)

```http
POST http://localhost:5000/api/v1/auth/register
Content-Type: application/json

{
    "username": "jane_smith",
    "email": "jane.smith@example.com",
    "password": "Password123",
    "full_name": "Jane Smith"
}
```

### 3. Login User

```http
POST http://localhost:5000/api/v1/auth/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "Password123",
    "device_info": "Postman Test",
    "ip_address": "127.0.0.1"
}
```

### 4. Create Transaction

```http
POST http://localhost:5000/api/v1/transaction
Content-Type: application/json
Authorization: Bearer {{access_token}}

{
    "type": "EXPENSE",
    "category_id": 1,
    "amount": 150000.50,
    "date": "2025-05-08T14:30:00Z",
    "description": "Lunch at restaurant",
    "formality_transaction": "BANK",
    "wallet_id": 1
}
```

## Test Cases

### Authentication Tests

| Test Name | Purpose | Expected Status |
|-----------|---------|-----------------|
| Register User (Full) | Test complete registration | 201 Created |
| Register User (Minimal) | Test minimal registration | 201 Created |
| Register User (Invalid Email) | Test email validation | 400 Bad Request |
| Register User (Weak Password) | Test password strength | 400 Bad Request |
| Register User (Invalid Date) | Test date format validation | 400 Bad Request |
| Login User | Test authentication | 200 OK |
| Logout User | Test session invalidation | 200 OK |

### Response Validation

Each request includes test scripts that validate:

- **Status Codes**: Correct HTTP status codes
- **Response Format**: Valid JSON structure
- **Data Fields**: Required fields present
- **Error Messages**: Appropriate error descriptions
- **Token Storage**: Auto-save tokens to environment

## Environment Variables

After successful login, these variables are automatically set:

- `access_token`: JWT access token for API calls
- `refresh_token`: JWT refresh token for token renewal
- `user_id`: Current user ID

## Error Handling

Common error responses:

### Validation Errors (400)
```json
{
    "status": "error",
    "message": "Password must contain at least one uppercase letter",
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2025-05-08T09:30:00.000Z"
}
```

### Authentication Errors (401)
```json
{
    "status": "error",
    "message": "Invalid username or password",
    "error_code": "AUTHENTICATION_FAILED",
    "timestamp": "2025-05-08T09:30:00.000Z"
}
```

### Conflict Errors (409)
```json
{
    "status": "error",
    "message": "Username already exists",
    "error_code": "CONFLICT",
    "timestamp": "2025-05-08T09:30:00.000Z"
}
```

## Tips for Testing

1. **Sequential Testing**: Run requests in order (Register → Login → Logout)
2. **Token Management**: Tokens are auto-saved, no manual copy-paste needed
3. **Data Cleanup**: Use different usernames for each test run
4. **Environment Switching**: Create separate environments for dev/staging/prod
5. **Batch Testing**: Use Postman's "Run Collection" feature for bulk testing

## Collection Features

- **Automatic Token Handling**: Login responses automatically set environment variables
- **Comprehensive Tests**: Each request includes validation scripts
- **Error Scenarios**: Multiple test cases for validation and error handling
- **Documentation**: Each request includes detailed descriptions
- **Environment Support**: Works with different base URLs

## Troubleshooting

### Connection Issues
- Ensure application is running on `localhost:5000`
- Check SSH tunnel is active if using remote database
- Verify `baseUrl` environment variable

### Authentication Issues
- Clear environment variables and re-login
- Check token expiration (access tokens expire in 1 hour)
- Verify user credentials

### Validation Errors
- Check request body format
- Verify required fields are present
- Ensure data types match API expectations

## Advanced Usage

### Custom Tests
Add custom test scripts in Postman:

```javascript
// Example: Check if response contains specific field
pm.test("Response contains user ID", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.data).to.have.property('id');
});

// Example: Validate response time
pm.test("Response time is less than 200ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});
```

### Dynamic Variables
Use Postman variables for dynamic data:

```javascript
// Generate random username
const randomUsername = `user_${Date.now()}`;
pm.environment.set("test_username", randomUsername);

// Use in request body
{
    "username": "{{test_username}}",
    "email": "{{test_username}}@example.com",
    "password": "Password123"
}
```

## Support

For Postman collection issues:
- Check API documentation: `docs/API_DOCUMENTATION.md`
- Review application logs for detailed errors
- Test with curl commands for debugging
- Contact development team for support
