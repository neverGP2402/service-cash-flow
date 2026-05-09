# Social Login Error Handling Guide

## Overview

Social login API handles various edge cases and provides specific error responses for different scenarios. This ensures a smooth user experience and clear feedback.

## Error Scenarios & Responses

### 1. Email Required from Provider

**Scenario:** User doesn't grant email permission to the social provider.

**Request:**
```json
{
    "provider": "google",
    "access_token": "valid_token_without_email_scope"
}
```

**Response (401 Unauthorized):**
```json
{
    "status": "error",
    "message": "Email is required from social provider. Please grant email permission.",
    "error_code": "EMAIL_REQUIRED",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

**Client Action:**
- Re-authenticate with the provider
- Request email permission scope
- Retry login

### 2. Email Not Verified

**Scenario:** User's email is not verified with the provider.

**Request:**
```json
{
    "provider": "github",
    "access_token": "valid_token_but_email_not_verified"
}
```

**Response (401 Unauthorized):**
```json
{
    "status": "error",
    "message": "Email address is not verified. Please verify your email with the provider first.",
    "error_code": "EMAIL_NOT_VERIFIED",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

**Client Action:**
- Guide user to verify email with provider
- Provide link to provider's email verification page
- Allow retry after verification

### 3. Invalid Social Token

**Scenario:** OAuth token is invalid, expired, or revoked.

**Request:**
```json
{
    "provider": "facebook",
    "access_token": "invalid_or_expired_token"
}
```

**Response (401 Unauthorized):**
```json
{
    "status": "error",
    "message": "Invalid social token",
    "error_code": "AUTHENTICATION_FAILED",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

**Client Action:**
- Clear stored token
- Re-authenticate with provider
- Get fresh access token

### 4. Provider API Unavailable

**Scenario:** Social provider API is down or rate limited.

**Response (500 Internal Server Error):**
```json
{
    "status": "error",
    "message": "Social login service temporarily unavailable",
    "error_code": "PROVIDER_UNAVAILABLE",
    "timestamp": "2025-05-08T10:30:00.000Z"
}
```

**Client Action:**
- Show friendly error message
- Suggest trying again later
- Offer alternative login methods

### 5. Email Already Exists

**Scenario:** User tries to login with social account but email is already registered with another method.

**Success Response (200 OK):**
```json
{
    "status": "success",
    "message": "Social login successful",
    "data": {
        "access_token": "jwt_token_here",
        "refresh_token": "refresh_token_here",
        "user": {
            "id": 123,
            "username": "existing_user",
            "email": "user@example.com",
            "full_name": "Existing User"
        },
        "is_new_user": false
    }
}
```

**Behavior:**
- Links to existing account
- Updates missing profile info (avatar, name)
- Logs user in normally

## Success Scenarios

### New User Registration

**Scenario:** First-time social login user.

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Account created successfully with social login",
    "data": {
        "access_token": "jwt_token_here",
        "refresh_token": "refresh_token_here",
        "user": {
            "id": 456,
            "username": "john_doe_123",
            "email": "newuser@example.com",
            "full_name": "John Doe",
            "avatar": "https://example.com/avatar.jpg"
        },
        "is_new_user": true
    }
}
```

**Client Action:**
- Show welcome message for new users
- Guide through profile setup
- Offer to complete additional information

### Existing User Login

**Scenario:** Returning social login user.

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Social login successful",
    "data": {
        "access_token": "jwt_token_here",
        "refresh_token": "refresh_token_here",
        "user": {
            "id": 123,
            "username": "john_doe",
            "email": "user@example.com",
            "full_name": "John Doe",
            "last_login_time": "2025-05-08T10:30:00Z"
        },
        "is_new_user": false
    }
}
```

**Client Action:**
- Normal login flow
- Update last login time
- Redirect to dashboard

## Client-Side Error Handling

### JavaScript Example

```javascript
async function handleSocialLogin(provider, accessToken) {
    try {
        const response = await fetch('/api/v1/auth/social-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                provider: provider,
                access_token: accessToken,
                device_info: 'Web App',
                ip_address: '127.0.0.1'
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            localStorage.setItem('access_token', data.data.access_token);
            localStorage.setItem('refresh_token', data.data.refresh_token);
            
            if (data.data.is_new_user) {
                // Show welcome flow for new users
                showWelcomeWizard(data.data.user);
            } else {
                // Normal login
                redirectToDashboard();
            }
        } else {
            // Handle specific error cases
            handleSocialLoginError(data);
        }
    } catch (error) {
        console.error('Social login failed:', error);
        showGenericError();
    }
}

function handleSocialLoginError(errorData) {
    switch (errorData.error_code) {
        case 'EMAIL_REQUIRED':
            showError('Please grant email permission to continue');
            // Re-authenticate with email scope
            reauthenticateWithEmailScope();
            break;
            
        case 'EMAIL_NOT_VERIFIED':
            showError('Please verify your email with the provider first');
            // Show verification instructions
            showEmailVerificationHelp();
            break;
            
        case 'AUTHENTICATION_FAILED':
            showError('Invalid or expired token. Please try logging in again.');
            // Clear token and re-authenticate
            clearSocialToken();
            break;
            
        case 'PROVIDER_UNAVAILABLE':
            showError('Service temporarily unavailable. Please try again later.');
            // Offer alternative login methods
            showAlternativeLoginOptions();
            break;
            
        default:
            showError('Login failed. Please try again.');
            break;
    }
}
```

### React Component Example

```jsx
import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const SocialLoginButton = ({ provider, icon, text }) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { login } = useAuth();

    const handleSocialLogin = async () => {
        setLoading(true);
        setError(null);
        
        try {
            // Get OAuth token from provider
            const token = await getSocialToken(provider);
            
            // Send to backend
            await loginWithSocial(provider, token);
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <button 
                onClick={handleSocialLogin}
                disabled={loading}
                className="social-login-btn"
            >
                {loading ? (
                    <Spinner />
                ) : (
                    <>
                        <img src={icon} alt={provider} />
                        {text}
                    </>
                )}
            </button>
            
            {error && (
                <div className="error-message">
                    {error}
                    {error.includes('email') && (
                        <button onClick={() => showEmailHelp(provider)}>
                            Need help with email permissions?
                        </button>
                    )}
                </div>
            )}
        </div>
    );
};
```

## Best Practices

### 1. Clear Error Messages

- Use user-friendly language
- Provide specific action steps
- Avoid technical jargon

### 2. Recovery Options

- Always provide a way to retry
- Offer alternative login methods
- Include help links

### 3. Progressive Enhancement

- Start with basic permissions
- Request additional scopes as needed
- Explain why each permission is needed

### 4. Security Considerations

- Validate tokens on every request
- Implement rate limiting
- Log authentication attempts

### 5. User Experience

- Show loading states
- Provide clear feedback
- Handle network failures gracefully

## Testing

### Postman Tests

```json
{
    "info": {
        "name": "Social Login Error Tests"
    },
    "item": [
        {
            "name": "Missing Email",
            "request": {
                "method": "POST",
                "body": {
                    "mode": "raw",
                    "raw": "{\"provider\": \"google\", \"access_token\": \"test_token\"}"
                }
            },
            "test": [
                "pm.test('Status code is 401', function () { pm.response.to.have.status(401); });",
                "pm.test('Error code is EMAIL_REQUIRED', function () { pm.expect(pm.response.json().error_code).to.eql('EMAIL_REQUIRED'); });"
            ]
        },
        {
            "name": "Invalid Token",
            "request": {
                "method": "POST",
                "body": {
                    "mode": "raw",
                    "raw": "{\"provider\": \"google\", \"access_token\": \"invalid_token\", \"email\": \"test@example.com\"}"
                }
            },
            "test": [
                "pm.test('Status code is 401', function () { pm.response.to.have.status(401); });",
                "pm.test('Error code is AUTHENTICATION_FAILED', function () { pm.expect(pm.response.json().error_code).to.eql('AUTHENTICATION_FAILED'); });"
            ]
        }
    ]
}
```

## Troubleshooting

### Common Issues

1. **Token Verification Fails**
   - Check provider API status
   - Verify token format
   - Check network connectivity

2. **Email Permission Issues**
   - Review OAuth scopes
   - Check provider console settings
   - Update consent screen

3. **Rate Limiting**
   - Implement caching
   - Use exponential backoff
   - Monitor API quotas

### Debug Tips

1. Log provider API responses
2. Check token expiration times
3. Verify OAuth app configuration
4. Test with provider's OAuth playground

## Support

For social login error handling issues:
- Check provider documentation for API changes
- Review OAuth app settings and scopes
- Verify backend token validation logic
- Contact development team for support
