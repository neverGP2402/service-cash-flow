# Login API Documentation

## Overview

The Login API provides secure authentication for the Cash Flow Management System. Users can log in using either their username or email address along with their password.

## Endpoint Details

### Login User

**Endpoint:** `POST /api/v1/auth/login`

**Description:** Authenticate user with username/email and password, return JWT tokens

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "Password123",
    "device_info": "Web App",
    "ip_address": "127.0.0.1"
}
```

**Field Descriptions:**

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| `username` | string | ✅ Yes | Username OR email address of the user |
| `password` | string | ✅ Yes | User's password (minimum 8 characters) |
| `device_info` | string | ❌ No | Device information for tracking |
| `ip_address` | string | ❌ No | Client IP address for security logging |

**Supported Login Formats:**

1. **Username Login:**
```json
{
    "username": "john_doe",
    "password": "Password123"
}
```

2. **Email Login:**
```json
{
    "username": "john.doe@example.com",
    "password": "Password123"
}
```

3. **Full Request with Device Info:**
```json
{
    "username": "john.doe@example.com",
    "password": "Password123",
    "device_info": "Chrome on Windows 10",
    "ip_address": "192.168.1.100"
}
```

## Response Examples

### Successful Login (200 OK)

```json
{
    "status": "success",
    "message": "Login successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3ODIzMzAwMCwianRpIjoiMTIzNDU2Nzg5LWY5MzItNGU2Zi1iMzU3LWQ2NzE4NzA5MjM5NyIsInR5cGUiOiJhY2Nlc3MiIsInN1YiI6IjEyMzQ1Njc4OS1mOTMyLTRlNmYtYjM1Ny1kNjcxODcwOTIzOTciLCJleHAiOjE3NzgyMzY2MDB9.signature",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzc4MjMzMDAwLCJqdGkiOiI5ODc2NTQzMjEtNzQwZi00YjA5LWFhNzYtZjM1MzFmNzM2ZDciLCJ0eXBlIjoicmVmcmVzaCIsInN1YiI6Ijk4NzY1NDMyMS03NDBmLTBiMDktYWE3Ni1mMzUzMWY3MzZkM2MiLCJleHAiOjE3ODgzOTc0MDB9.signature",
        "user": {
            "id": 123,
            "username": "john_doe",
            "email": "john.doe@example.com",
            "full_name": "John Doe",
            "avatar": "https://example.com/avatars/john.jpg",
            "status": "ACTIVE",
            "last_login_time": "2025-05-08T10:30:00Z",
            "register_date": "2025-01-15T08:00:00Z"
        }
    },
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

### Error Responses

#### 400 Bad Request - Missing Fields

```json
{
    "status": "error",
    "message": "Request body is required",
    "error_code": "BAD_REQUEST",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

#### 400 Bad Request - Validation Error

```json
{
    "status": "error",
    "message": "Username must be at least 3 characters long",
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

#### 401 Unauthorized - Invalid Credentials

```json
{
    "status": "error",
    "message": "Invalid username or password",
    "error_code": "AUTHENTICATION_FAILED",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

#### 401 Unauthorized - Account Inactive

```json
{
    "status": "error",
    "message": "Account is inactive. Please contact support.",
    "error_code": "ACCOUNT_INACTIVE",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

#### 429 Too Many Requests - Rate Limited

```json
{
    "status": "error",
    "message": "Too many login attempts. Please try again later.",
    "error_code": "RATE_LIMIT_EXCEEDED",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

## Authentication Flow

### 1. User Identification

The system accepts either:
- **Username:** `john_doe`, `jane_smith`, etc.
- **Email:** `john.doe@example.com`, `jane.smith@company.com`, etc.

### 2. Password Verification

- Passwords are hashed using bcrypt
- Minimum 8 characters required
- Case-sensitive comparison

### 3. Session Creation

- JWT access token (expires in 1 hour)
- JWT refresh token (expires in 7 days)
- Session tracking with device info and IP

### 4. Response Data

**Access Token:**
- Type: JWT (JSON Web Token)
- Algorithm: HS256
- Expiration: 1 hour
- Usage: Include in Authorization header: `Bearer <token>`

**Refresh Token:**
- Type: JWT (JSON Web Token)
- Algorithm: HS256
- Expiration: 7 days
- Usage: Token renewal API

**User Data:**
- Basic profile information
- Last login timestamp
- Account status

## Security Features

### Password Security

```json
// Password requirements
{
    "min_length": 8,
    "max_length": 255,
    "required_patterns": [
        "uppercase_letter",
        "lowercase_letter", 
        "digit"
    ]
}
```

### Rate Limiting

- **Maximum attempts:** 5 per minute per IP
- **Lockout duration:** 15 minutes after 5 failed attempts
- **Account lockout:** 30 minutes after 10 failed attempts

### Session Security

- **Device tracking:** Log device information
- **IP tracking:** Monitor login locations
- **Token rotation:** Refresh tokens invalidated on use
- **Concurrent sessions:** Maximum 3 active sessions

## Client Implementation Examples

### JavaScript (Axios)

```javascript
// Login function
async function login(username, password, deviceInfo = '') {
    try {
        const response = await axios.post('/api/v1/auth/login', {
            username: username, // Can be username or email
            password: password,
            device_info: deviceInfo,
            ip_address: await getClientIP()
        });

        const { access_token, refresh_token, user } = response.data.data;
        
        // Store tokens securely
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('user', JSON.stringify(user));
        
        // Set default authorization header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        return { success: true, user };
        
    } catch (error) {
        const errorMessage = error.response?.data?.message || 'Login failed';
        return { success: false, error: errorMessage };
    }
}

// Usage examples
const result1 = await login('john_doe', 'Password123'); // Username login
const result2 = await login('john.doe@example.com', 'Password123'); // Email login

// Error handling
if (!result1.success) {
    console.error('Login failed:', result1.error);
    // Show error message to user
    showLoginError(result1.error);
}
```

### React Hook

```jsx
import { useState } from 'react';
import { useAuth } from './AuthContext';

const useLogin = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { setUser, setTokens } = useAuth();

    const login = async (username, password) => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username, // Accepts both username and email
                    password: password,
                    device_info: navigator.userAgent,
                    ip_address: await getClientIP()
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Store authentication data
                localStorage.setItem('access_token', data.data.access_token);
                localStorage.setItem('refresh_token', data.data.refresh_token);
                localStorage.setItem('user', JSON.stringify(data.data.user));
                
                // Update auth context
                setUser(data.data.user);
                setTokens({
                    access: data.data.access_token,
                    refresh: data.data.refresh_token
                });
                
                return { success: true };
            } else {
                throw new Error(data.message);
            }
            
        } catch (err) {
            const errorMessage = err.message || 'Login failed';
            setError(errorMessage);
            return { success: false, error: errorMessage };
        } finally {
            setLoading(false);
        }
    };

    return { login, loading, error };
};

// Component usage
const LoginForm = () => {
    const { login, loading, error } = useLogin();
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        const result = await login(formData.username, formData.password);
        
        if (result.success) {
            window.location.href = '/dashboard';
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Username or Email"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                required
            />
            <input
                type="password"
                placeholder="Password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
            />
            <button type="submit" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
            </button>
            {error && <div className="error">{error}</div>}
        </form>
    );
};
```

### Python (Requests)

```python
import requests
from typing import Dict, Any, Optional

class AuthClient:
    def __init__(self, base_url: str = 'http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, username: str, password: str, device_info: str = '', ip_address: str = '') -> Optional[Dict[str, Any]]:
        """Login with username or email"""
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/auth/login',
                json={
                    'username': username,  # Can be username or email
                    'password': password,
                    'device_info': device_info,
                    'ip_address': ip_address
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': data['data']
                }
            else:
                error_data = response.json()
                return {
                    'success': False,
                    'error': error_data.get('message', 'Login failed'),
                    'error_code': error_data.get('error_code')
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
    
    def set_auth_headers(self, access_token: str):
        """Set authorization headers for future requests"""
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}'
        })

# Usage examples
auth = AuthClient()

# Username login
result1 = auth.login('john_doe', 'Password123')

# Email login  
result2 = auth.login('john.doe@example.com', 'Password123')

# Handle response
if result1['success']:
    tokens = result1['data']
    auth.set_auth_headers(tokens['access_token'])
    print(f"Login successful! User: {tokens['user']['username']}")
else:
    print(f"Login failed: {result1['error']}")
```

## Testing

### Postman Collection

```json
{
    "info": {
        "name": "Login API Tests"
    },
    "item": [
        {
            "name": "Login with Username",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"username\": \"john_doe\",\n    \"password\": \"Password123\",\n    \"device_info\": \"Postman Test\",\n    \"ip_address\": \"127.0.0.1\"\n}"
                },
                "url": {
                    "raw": "{{baseUrl}}/api/v1/auth/login",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "v1", "auth", "login"]
                }
            }
        },
        {
            "name": "Login with Email",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"username\": \"john.doe@example.com\",\n    \"password\": \"Password123\"\n}"
                },
                "url": {
                    "raw": "{{baseUrl}}/api/v1/auth/login",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "v1", "auth", "login"]
                }
            }
        },
        {
            "name": "Invalid Credentials",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"username\": \"invalid_user\",\n    \"password\": \"wrong_password\"\n}"
                },
                "url": {
                    "raw": "{{baseUrl}}/api/v1/auth/login",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "v1", "auth", "login"]
                }
            },
            "test": [
                "pm.test('Status code is 401', function () { pm.response.to.have.status(401); });",
                "pm.test('Error message about credentials', function () { pm.expect(pm.response.json().message).to.include('Invalid username or password'); });"
            ]
        }
    ]
}
```

### cURL Commands

```bash
# Login with username
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "Password123",
    "device_info": "cURL Test",
    "ip_address": "127.0.0.1"
  }'

# Login with email
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john.doe@example.com",
    "password": "Password123"
  }'

# Test invalid credentials
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nonexistent",
    "password": "wrong"
  }' -v
```

## Best Practices

### 1. Security

- **Always use HTTPS** in production
- **Validate input** on client side before sending
- **Store tokens securely** (httpOnly cookies or secure storage)
- **Implement token refresh** before expiration
- **Log out properly** to invalidate sessions

### 2. User Experience

- **Clear error messages** for different failure types
- **Loading states** during authentication
- **Remember me** option with persistent sessions
- **Password strength indicators** during registration
- **Forgot password** flow for recovery

### 3. Error Handling

- **Network failures**: Show retry options
- **Invalid credentials**: Suggest password reset
- **Account locked**: Provide support contact
- **Rate limiting**: Show countdown timer

### 4. Performance

- **Debounce login requests** to prevent duplicate calls
- **Cache user session** to reduce API calls
- **Optimize token refresh** timing
- **Monitor login metrics** for optimization

## Troubleshooting

### Common Issues

1. **"Invalid username or password"**
   - Check for typos in username/password
   - Verify account exists and is active
   - Try with email instead of username

2. **Rate limiting errors**
   - Wait for lockout period to expire
   - Check for automated login attempts
   - Contact support if needed

3. **Network errors**
   - Verify API endpoint is accessible
   - Check internet connectivity
   - Try different network

4. **Token issues**
   - Clear stored tokens and re-login
   - Check system time synchronization
   - Verify token format

### Debug Tips

1. **Check network requests** in browser dev tools
2. **Verify request format** matches documentation
3. **Test with different credentials** to isolate issues
4. **Check server logs** for detailed errors

## Support

For login API issues:
- Check user credentials in database
- Verify email/username uniqueness
- Review authentication logs
- Contact development team for support
