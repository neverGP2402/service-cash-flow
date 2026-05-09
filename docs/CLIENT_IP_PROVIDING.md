# Client IP Providing Guide

## Overview

The Cash Flow Management API supports client-provided IP addresses to give applications full control over IP detection, while maintaining fallback support for automatic detection.

## IP Address Priority

The system uses the following priority order for IP detection:

### 1. Client-Provided IP (Highest Priority)
**Source:** `ip_address` field in request body
**Use Case:** Client wants to control IP detection
**Advantage:** Reliable IP from client's perspective

### 2. Automatic Detection (Fallback)
**Source:** HTTP headers and server detection
**Use Case:** Client doesn't provide IP or wants automatic detection
**Advantage:** Works with proxy/load balancer setups

## API Usage

### Regular Login with Client IP

```json
{
    "username": "john_doe",
    "password": "Password123",
    "device_info": "Web App",
    "ip_address": "203.0.113.45"
}
```

### Social Login with Client IP

```json
{
    "provider": "google",
    "access_token": "ya29.a0AfH6SMC...",
    "email": "user@gmail.com",
    "name": "John Doe",
    "device_info": "Web App",
    "ip_address": "203.0.113.45"
}
```

### Automatic IP Detection (No IP Provided)

```json
{
    "username": "john_doe",
    "password": "Password123",
    "device_info": "Web App"
    // ip_address not provided - will use automatic detection
}
```

## Client Implementation Examples

### JavaScript (Browser)

```javascript
// Get client's real IP address
async function getClientIP() {
    try {
        // Method 1: Using external service
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.warn('Could not get external IP:', error);
        
        try {
            // Method 2: Using WebRTC (more complex but no external service)
            return await getIPViaWebRTC();
        } catch (rtcError) {
            console.warn('WebRTC IP detection failed:', rtcError);
            return null; // Let server handle detection
        }
    }
}

// Login with client-provided IP
async function loginWithClientIP(username, password) {
    const clientIP = await getClientIP();
    
    const loginData = {
        username: username,
        password: password,
        device_info: navigator.userAgent,
        ip_address: clientIP || undefined  // Send if available, otherwise let server detect
    };
    
    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            localStorage.setItem('access_token', result.data.access_token);
            console.log('Login successful with IP:', clientIP);
            return { success: true, data: result.data };
        } else {
            return { success: false, error: result.message };
        }
    } catch (error) {
        console.error('Login failed:', error);
        return { success: false, error: 'Network error' };
    }
}

// Usage
const result = await loginWithClientIP('john_doe', 'Password123');
if (result.success) {
    console.log('Logged in with IP detection');
} else {
    console.error('Login failed:', result.error);
}
```

### React Component

```jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';

const LoginForm = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        device_info: '',
        ip_address: ''
    });
    const [loading, setLoading] = useState(false);
    const [detectingIP, setDetectingIP] = useState(false);
    const { login } = useAuth();

    // Auto-detect IP on component mount
    useEffect(() => {
        detectClientIP();
    }, []);

    const detectClientIP = async () => {
        setDetectingIP(true);
        try {
            const ip = await getClientIP();
            setFormData(prev => ({ ...prev, ip_address: ip }));
        } catch (error) {
            console.warn('IP detection failed, using server detection:', error);
        } finally {
            setDetectingIP(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        const result = await login(formData);
        
        if (result.success) {
            // Successful login
            window.location.href = '/dashboard';
        } else {
            // Handle error
            alert(result.error);
        }
        
        setLoading(false);
    };

    return (
        <div className="login-form">
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Username or Email:</label>
                    <input
                        type="text"
                        value={formData.username}
                        onChange={(e) => setFormData({...formData, username: e.target.value})}
                        required
                    />
                </div>
                
                <div className="form-group">
                    <label>Password:</label>
                    <input
                        type="password"
                        value={formData.password}
                        onChange={(e) => setFormData({...formData, password: e.target.value})}
                        required
                    />
                </div>
                
                <div className="form-group">
                    <label>IP Address (Optional):</label>
                    <input
                        type="text"
                        value={formData.ip_address}
                        onChange={(e) => setFormData({...formData, ip_address: e.target.value})}
                        placeholder="Auto-detect if empty"
                        disabled={detectingIP}
                    />
                    {detectingIP && <span className="detecting">Detecting IP...</span>}
                    <button 
                        type="button" 
                        onClick={detectClientIP}
                        disabled={detectingIP}
                    >
                        Detect My IP
                    </button>
                </div>
                
                <div className="form-group">
                    <label>Device Info:</label>
                    <input
                        type="text"
                        value={formData.device_info}
                        onChange={(e) => setFormData({...formData, device_info: e.target.value})}
                        placeholder={navigator.userAgent}
                    />
                </div>
                
                <button type="submit" disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </form>
        </div>
    );
};

// Helper function to get client IP
async function getClientIP() {
    try {
        // Try multiple IP detection services
        const services = [
            'https://api.ipify.org?format=json',
            'https://ipapi.co/json/',
            'https://api.ipgeolocation.io/ipgeo'
        ];
        
        for (const service of services) {
            try {
                const response = await fetch(service);
                const data = await response.json();
                
                // Different services have different response formats
                const ip = data.ip || data.ip_address || data.query;
                
                if (ip && isValidIP(ip)) {
                    return ip;
                }
            } catch (error) {
                continue; // Try next service
            }
        }
        
        throw new Error('Could not detect IP from any service');
    } catch (error) {
        console.error('IP detection failed:', error);
        throw error;
    }
}

function isValidIP(ip) {
    // Basic IP validation
    const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return ipRegex.test(ip);
}
```

### Python Client

```python
import requests
import socket
from typing import Optional

class AuthClient:
    def __init__(self, base_url: str = 'http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_client_ip(self) -> Optional[str]:
        """Get client's public IP address"""
        try:
            # Method 1: External service
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                return response.json().get('ip')
        except:
            pass
        
        try:
            # Method 2: Another external service
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                return response.json().get('ip')
        except:
            pass
        
        try:
            # Method 3: Local IP (fallback)
            # Connect to external host to get local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            pass
        
        return None  # Let server handle detection
    
    def login(self, username: str, password: str, use_client_ip: bool = True):
        """Login with optional client IP detection"""
        login_data = {
            'username': username,
            'password': password,
            'device_info': 'Python Client'
        }
        
        if use_client_ip:
            client_ip = self.get_client_ip()
            if client_ip:
                login_data['ip_address'] = client_ip
                print(f"Using client-provided IP: {client_ip}")
            else:
                print("IP detection failed, using server detection")
        else:
            print("Using server-side IP detection only")
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/auth/login',
                json=login_data,
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
                    'error': error_data.get('message', 'Login failed')
                }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }

# Usage examples
auth = AuthClient()

# Login with client IP detection
result1 = auth.login('john_doe', 'Password123', use_client_ip=True)

# Login with server-side detection only
result2 = auth.login('john_doe', 'Password123', use_client_ip=False)

if result1['success']:
    print("Login successful!")
    print(f"User data: {result1['data']['user']}")
else:
    print(f"Login failed: {result1['error']}")
```

### Mobile App (React Native)

```javascript
import { NativeModules, Platform } from 'react-native';

// Get device IP address
const getDeviceIP = async () => {
    try {
        if (Platform.OS === 'ios') {
            // iOS specific IP detection
            const { IPAddress } = NativeModules.NetworkInfo;
            const ip = await IPAddress.getPublicIP();
            return ip;
        } else if (Platform.OS === 'android') {
            // Android specific IP detection
            const { WifiInfo } = NativeModules.NetworkInfo;
            const ip = await WifiInfo.getPublicIP();
            return ip;
        } else {
            // Web fallback
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            return data.ip;
        }
    } catch (error) {
        console.warn('IP detection failed:', error);
        return null;
    }
};

// Login with device IP
const login = async (username, password) => {
    const deviceIP = await getDeviceIP();
    
    const loginData = {
        username: username,
        password: password,
        device_info: `${Platform.OS} App`,
        ip_address: deviceIP || undefined
    };
    
    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Store tokens
            await AsyncStorage.setItem('access_token', result.data.access_token);
            await AsyncStorage.setItem('user', JSON.stringify(result.data.user));
            
            return { success: true, data: result.data };
        } else {
            return { success: false, error: result.message };
        }
    } catch (error) {
        return { success: false, error: 'Network error' };
    }
};
```

## Testing Client IP Detection

### 1. Manual Testing

```bash
# Test with explicit IP
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "test",
    "ip_address": "203.0.113.45"
  }'

# Test without IP (server detection)
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "test"
  }'
```

### 2. Postman Testing

```json
{
    "name": "Client IP Test",
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
            "raw": "{\n    \"username\": \"test\",\n    \"password\": \"test\",\n    \"ip_address\": \"203.0.113.45\",\n    \"device_info\": \"Postman Test\"\n}"
        }
    }
}
```

## Security Considerations

### 1. IP Validation

```javascript
function isValidIP(ip) {
    // IPv4 validation
    const ipv4Regex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    
    // IPv6 validation (simplified)
    const ipv6Regex = /^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/;
    
    return ipv4Regex.test(ip) || ipv6Regex.test(ip);
}

// Only use validated IPs
const clientIP = await getClientIP();
if (clientIP && isValidIP(clientIP)) {
    // Proceed with client IP
} else {
    // Let server handle detection
}
```

### 2. Privacy Considerations

- **Inform users** about IP detection
- **Provide opt-out** option
- **Store IP securely** if needed
- **Follow GDPR** for EU users

### 3. Rate Limiting

```javascript
// Implement client-side rate limiting
const loginAttempts = {};
const MAX_ATTEMPTS = 5;
const LOCKOUT_TIME = 15 * 60 * 1000; // 15 minutes

function canAttemptLogin(ip) {
    const now = Date.now();
    const attempts = loginAttempts[ip] || [];
    
    // Remove old attempts
    const validAttempts = attempts.filter(time => now - time < LOCKOUT_TIME);
    
    return validAttempts.length < MAX_ATTEMPTS;
}
```

## Best Practices

### 1. Progressive Enhancement

1. **Start with server detection** (always works)
2. **Add client detection** (more reliable)
3. **Provide fallback** (graceful degradation)
4. **User control** (let user choose)

### 2. Error Handling

```javascript
async function robustLogin(username, password) {
    try {
        // Try client IP detection first
        const clientIP = await getClientIP();
        
        const loginData = {
            username,
            password,
            device_info: navigator.userAgent,
            ip_address: clientIP || undefined
        };
        
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData)
        });
        
        return await response.json();
        
    } catch (error) {
        console.error('Login failed, retrying without IP:', error);
        
        // Fallback: try without IP detection
        const fallbackData = {
            username,
            password,
            device_info: navigator.userAgent
            // ip_address: undefined - let server detect
        };
        
        const fallbackResponse = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(fallbackData)
        });
        
        return await fallbackResponse.json();
    }
}
```

### 3. User Experience

- **Show IP detection status** to user
- **Provide manual override** option
- **Cache IP** for session duration
- **Handle failures** gracefully

## Troubleshooting

### Common Issues

1. **IP Detection Fails**
   - Check external service availability
   - Verify network connectivity
   - Try different IP services

2. **Invalid IP Format**
   - Validate IP format before sending
   - Use proper IP validation regex
   - Handle IPv4 vs IPv6

3. **Rate Limiting**
   - Implement exponential backoff
   - Use different endpoints for IP detection
   - Cache results appropriately

### Debug Tips

1. **Log IP detection attempts**
2. **Monitor external service status**
3. **Test with known IPs** for validation
4. **Check CORS headers** for cross-origin issues

## Support

For client IP detection issues:
- Test with different IP detection services
- Verify network connectivity
- Check external service status
- Review implementation examples above
