# IP Address Detection Guide

## Overview

The Cash Flow Management API implements robust IP address detection to handle various deployment scenarios including proxies, load balancers, and CDNs.

## IP Detection Methods

The system checks IP addresses in the following order of priority:

### 1. X-Forwarded-For Header
**Use Case:** Behind reverse proxy (nginx, Apache, etc.)
**Format:** `X-Forwarded-For: <client-ip>, <proxy1-ip>, <proxy2-ip>`
**Example:** `X-Forwarded-For: 203.0.113.45, 10.0.0.1, 192.168.1.1`

### 2. X-Real-IP Header
**Use Case:** Behind load balancer (AWS ELB, Nginx, etc.)
**Format:** `X-Real-IP: <client-ip>`
**Example:** `X-Real-IP: 203.0.113.45`

### 3. X-Client-IP Header
**Use Case:** Custom proxy configurations
**Format:** `X-Client-IP: <client-ip>`
**Example:** `X-Client-IP: 203.0.113.45`

### 4. CF-Connecting-IP Header
**Use Case:** Behind Cloudflare CDN
**Format:** `CF-Connecting-IP: <client-ip>`
**Example:** `CF-Connecting-IP: 203.0.113.45`

### 5. request.remote_addr
**Use Case:** Direct connection (no proxy)
**Format:** Direct IP address
**Example:** `203.0.113.45`

### 6. Fallback
**Use Case:** Development or testing
**Value:** `127.0.0.1`

## Implementation Details

### Python/Flask Implementation

```python
def _get_client_ip(self):
    """Get client IP address from multiple sources"""
    # Try different sources in order of reliability
    
    # 1. X-Forwarded-For header (when behind proxy)
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return ip
    
    # 2. X-Real-IP header (when behind load balancer)
    if request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
        return ip
    
    # 3. X-Client-IP header
    if request.headers.get('X-Client-IP'):
        ip = request.headers.get('X-Client-IP')
        return ip
    
    # 4. CF-Connecting-IP header (Cloudflare)
    if request.headers.get('CF-Connecting-IP'):
        ip = request.headers.get('CF-Connecting-IP')
        return ip
    
    # 5. request.remote_addr (direct connection)
    if request.remote_addr:
        return request.remote_addr
    
    # 6. Fallback to localhost for development
    return '127.0.0.1'
```

## Deployment Scenarios

### 1. Direct Connection
**Setup:** Application directly exposed to internet
**IP Source:** `request.remote_addr`
**Example:** Client → Internet → Your Server

### 2. Nginx Reverse Proxy
**Setup:** Nginx → Your Application
**Nginx Config:**
```nginx
server {
    listen 80;
    server_name yourapp.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. AWS Application Load Balancer
**Setup:** AWS ALB → Your Application
**ALB Configuration:**
```yaml
# AWS ALB automatically adds X-Forwarded-For headers
# No additional configuration needed
```

### 4. Cloudflare CDN
**Setup:** Cloudflare → Your Application
**Cloudflare Features:**
- Automatically adds `CF-Connecting-IP` header
- May also add `CF-Ray` header for request tracing

### 5. Docker/Container Environment
**Setup:** Docker Container → Your Application
**Docker Compose:**
```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - TRUSTED_PROXIES=nginx,cloudflare
```

## Security Considerations

### 1. IP Spoofing Prevention

```python
def _is_valid_ip(self, ip):
    """Validate IP address format and range"""
    try:
        ipaddress.ip_address(ip)
        # Add additional validation as needed
        return True
    except ValueError:
        return False

def _get_client_ip(self):
    """Get client IP address with validation"""
    ip = self._get_raw_client_ip()
    
    if self._is_valid_ip(ip):
        return ip
    else:
        # Log suspicious IP attempts
        logger.warning(f"Invalid IP address detected: {ip}")
        return '127.0.0.1'
```

### 2. Proxy Configuration

```python
# Configure trusted proxies in Flask
app.wsgi_app = ProxyFix(
    app.wsgi_app, 
    x_for=1, 
    x_proto=1, 
    x_host=1, 
    x_port=1,
    x_prefix=1
)
```

### 3. Rate Limiting by IP

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,  # Uses the same IP detection logic
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/v1/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Your login logic here
    pass
```

## Testing IP Detection

### 1. Local Testing

```bash
# Test direct connection
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'

# Test with X-Forwarded-For header
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -H "X-Forwarded-For: 203.0.113.45" \
  -d '{"username": "test", "password": "test"}'
```

### 2. Postman Testing

```json
{
    "name": "IP Detection Test",
    "request": {
        "method": "POST",
        "header": [
            {
                "key": "Content-Type",
                "value": "application/json"
            },
            {
                "key": "X-Forwarded-For",
                "value": "203.0.113.45"
            }
        ],
        "body": {
            "mode": "raw",
            "raw": "{\"username\": \"test\", \"password\": \"test\"}"
        }
    }
}
```

### 3. Production Testing

```javascript
// Client-side IP detection test
async function testIPDetection() {
    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Forwarded-For': '203.0.113.45'  // Simulate proxy
            },
            body: JSON.stringify({
                username: 'test',
                password: 'test',
                device_info: navigator.userAgent
            })
        });
        
        const data = await response.json();
        console.log('Server detected IP:', data.ip_address);
        
        // Check server logs to verify IP detection
    } catch (error) {
        console.error('IP detection test failed:', error);
    }
}
```

## Configuration Examples

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/yourapp
server {
    listen 80;
    server_name yourapp.com;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    
    # Proxy headers
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Apache Configuration

```apache
# /etc/apache2/sites-available/yourapp.conf
<VirtualHost *:80>
    ServerName yourapp.com
    
    ProxyPreserveHost On
    ProxyRequests Off
    
    ProxyPass / http://localhost:5000/
    ProxyPassReverse / http://localhost:5000/
    
    # IP forwarding headers
    RequestHeader set X-Forwarded-Proto "https"
    RequestHeader set X-Forwarded-For "%{REMOTE_ADDR}s"
</VirtualHost>
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Environment variables for proxy detection
ENV TRUSTED_PROXIES=nginx,apache,cloudflare
ENV BEHIND_PROXY=true

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Troubleshooting

### Common Issues

1. **IP Always Shows 127.0.0.1**
   - Check if running behind proxy
   - Verify proxy configuration
   - Check firewall settings

2. **Incorrect IP in Production**
   - Verify proxy headers are being passed
   - Check load balancer configuration
   - Test with different headers

3. **Missing IP Headers**
   - Ensure proxy is configured to forward headers
   - Check CDN settings
   - Verify reverse proxy configuration

### Debug Logging

```python
import logging

# Configure logging for IP detection
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def _get_client_ip(self):
    """Get client IP address with debug logging"""
    
    # Log all available headers
    logger.debug(f"All headers: {dict(request.headers)}")
    
    # Log each IP source attempt
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        logger.debug(f"Using X-Forwarded-For: {ip}")
        return ip
    
    # ... continue for other sources
    
    logger.debug(f"Final IP detected: {ip}")
    return ip
```

## Best Practices

1. **Always validate IP format** before using
2. **Log IP detection** for debugging
3. **Configure proxies properly** in your infrastructure
4. **Test in different environments** (dev, staging, prod)
5. **Monitor IP patterns** for security analysis
6. **Use HTTPS** to prevent header tampering
7. **Implement rate limiting** based on detected IP
8. **Document your proxy setup** for future maintenance

## Support

For IP detection issues:
- Check your proxy/load balancer configuration
- Verify headers are being forwarded correctly
- Review application logs for IP detection
- Test with different deployment scenarios
