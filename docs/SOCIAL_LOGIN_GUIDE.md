# Social Login Integration Guide

## Overview

The Cash Flow Management API supports OAuth2.0 login with Google, GitHub, and Facebook. This allows users to register and login using their existing social media accounts.

## Supported Providers

- **Google** - Google OAuth 2.0
- **GitHub** - GitHub OAuth 2.0  
- **Facebook** - Facebook Graph API

## API Endpoints

### Social Login

**Endpoint:** `POST /api/v1/auth/social-login`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "provider": "google",
    "access_token": "ya29.a0AfH6SMC...",
    "email": "user@gmail.com",
    "name": "John Doe",
    "avatar": "https://lh3.googleusercontent.com/...",
    "device_info": "Web App",
    "ip_address": "127.0.0.1"
}
```

**Required Fields:**
- `provider` (string): `google`, `github`, or `facebook`
- `access_token` (string): OAuth access token from provider

**Optional Fields:**
- `email` (string): User's email (for verification)
- `name` (string): User's full name
- `avatar` (string): Profile picture URL
- `device_info` (string): Device information
- `ip_address` (string): Client IP address

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Social login successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 123,
            "username": "john_doe",
            "email": "user@gmail.com",
            "full_name": "John Doe",
            "avatar": "https://lh3.googleusercontent.com/...",
            "status": "ACTIVE",
            "last_login_time": "2025-05-08T10:30:00Z"
        }
    }
}
```

## Provider-Specific Implementation

### Google OAuth 2.0

#### 1. Setup Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google+ API and Google OAuth2 API
4. Create OAuth 2.0 Client ID
5. Add authorized redirect URIs

#### 2. Client-Side Implementation

```javascript
// Google Sign-In
function initGoogleSignIn() {
    gapi.load('auth2', function() {
        gapi.auth2.init({
            client_id: 'YOUR_GOOGLE_CLIENT_ID',
            scope: 'profile email'
        }).then(function() {
            // Render sign-in button
            gapi.signin2.render('google-signin-btn', {
                'onsuccess': onGoogleSignIn,
                'theme': 'dark'
            });
        });
    });
}

function onGoogleSignIn(googleUser) {
    const profile = googleUser.getBasicProfile();
    const authResponse = googleUser.getAuthResponse();
    
    // Send to backend
    fetch('/api/v1/auth/social-login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            provider: 'google',
            access_token: authResponse.access_token,
            email: profile.getEmail(),
            name: profile.getName(),
            avatar: profile.getImageUrl()
        })
    })
    .then(response => response.json())
    .then(data => {
        // Handle successful login
        localStorage.setItem('access_token', data.data.access_token);
        window.location.href = '/dashboard';
    })
    .catch(error => {
        console.error('Google login failed:', error);
    });
}
```

#### 3. HTML Integration

```html
<!-- Google Sign-In -->
<script src="https://apis.google.com/js/platform.js" async defer></script>
<div id="google-signin-btn" class="g-signin2" data-width="300" data-height="50" data-longtitle="true"></div>
```

### GitHub OAuth 2.0

#### 1. Setup GitHub OAuth

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create new OAuth App
3. Set callback URL
4. Note Client ID and Client Secret

#### 2. Client-Side Implementation

```javascript
// GitHub OAuth
function loginWithGitHub() {
    const clientId = 'YOUR_GITHUB_CLIENT_ID';
    const redirectUri = encodeURIComponent('YOUR_CALLBACK_URL');
    const scope = 'user:email';
    
    const authUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
    
    // Open popup
    const popup = window.open(authUrl, 'github-login', 'width=600,height=600');
    
    // Listen for callback
    window.addEventListener('message', function(event) {
        if (event.data.type === 'github-auth') {
            popup.close();
            handleGitHubAuth(event.data.code);
        }
    });
}

function handleGitHubAuth(code) {
    // Exchange code for token (this should be done on backend)
    fetch('/api/v1/auth/github-callback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        // Use the access token from backend
        return fetch('/api/v1/auth/social-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                provider: 'github',
                access_token: data.access_token
            })
        });
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('access_token', data.data.access_token);
        window.location.href = '/dashboard';
    });
}
```

### Facebook OAuth 2.0

#### 1. Setup Facebook OAuth

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create new app
3. Add Facebook Login product
4. Configure OAuth redirect URIs

#### 2. Client-Side Implementation

```javascript
// Facebook Login
function initFacebookLogin() {
    window.fbAsyncInit = function() {
        FB.init({
            appId: 'YOUR_FACEBOOK_APP_ID',
            cookie: true,
            xfbml: true,
            version: 'v18.0'
        });
    };
    
    (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = 'https://connect.facebook.net/en_US/sdk.js';
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
}

function loginWithFacebook() {
    FB.login(function(response) {
        if (response.authResponse) {
            // Send to backend
            fetch('/api/v1/auth/social-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    provider: 'facebook',
                    access_token: response.authResponse.accessToken
                })
            })
            .then(response => response.json())
            .then(data => {
                localStorage.setItem('access_token', data.data.access_token);
                window.location.href = '/dashboard';
            })
            .catch(error => {
                console.error('Facebook login failed:', error);
            });
        }
    }, { scope: 'email,public_profile' });
}
```

#### 3. HTML Integration

```html
<!-- Facebook Login -->
<div id="fb-root"></div>
<script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js"></script>
<button onclick="loginWithFacebook()">Login with Facebook</button>
```

## Security Considerations

### Token Validation

The backend validates tokens by making API calls to the provider:

- **Google**: `https://www.googleapis.com/oauth2/v2/userinfo?access_token={token}`
- **GitHub**: `https://api.github.com/user` with Authorization header
- **Facebook**: `https://graph.facebook.com/me?fields=id,name,email,picture&access_token={token}`

### Rate Limiting

- Provider APIs have rate limits
- Implement caching for user info
- Handle API failures gracefully

### Email Verification

- Only verified emails are accepted
- GitHub requires separate API call for emails
- Facebook and Google provide email verification status

## Error Handling

### Common Errors

**400 Bad Request:**
```json
{
    "status": "error",
    "message": "Provider must be one of: google, github, facebook",
    "error_code": "VALIDATION_ERROR"
}
```

**401 Unauthorized:**
```json
{
    "status": "error", 
    "message": "Invalid social token",
    "error_code": "AUTHENTICATION_FAILED"
}
```

**500 Server Error:**
```json
{
    "status": "error",
    "message": "Social login service temporarily unavailable",
    "error_code": "INTERNAL_SERVER_ERROR"
}
```

## Testing

### Postman Collection

```json
{
    "info": {
        "name": "Social Login Tests"
    },
    "item": [
        {
            "name": "Google Login",
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
                    "raw": "{\n    \"provider\": \"google\",\n    \"access_token\": \"test_google_token\",\n    \"email\": \"test@gmail.com\",\n    \"name\": \"Test User\"\n}"
                },
                "url": {
                    "raw": "{{baseUrl}}/api/v1/auth/social-login",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "v1", "auth", "social-login"]
                }
            }
        }
    ]
}
```

### Manual Testing

1. Get real access token from provider
2. Send POST request to `/api/v1/auth/social-login`
3. Verify response contains user data and tokens

## Best Practices

1. **Use HTTPS** for all OAuth flows
2. **Validate tokens** on every request
3. **Implement rate limiting** for social login endpoints
4. **Handle provider outages** gracefully
5. **Store minimal user data** required for your app
6. **Provide logout** for social accounts
7. **Update user info** periodically from provider
8. **Implement refresh token** rotation for security

## Troubleshooting

### Common Issues

1. **Invalid Token**: Check token expiration and scope
2. **Email Missing**: Ensure proper OAuth scopes are requested
3. **Rate Limits**: Implement backoff and retry logic
4. **CORS Issues**: Configure proper origins in backend

### Debug Tips

1. Log provider API responses
2. Check network requests in browser dev tools
3. Verify OAuth app configuration
4. Test with provider's OAuth playground

## Support

For social login integration issues:
- Check provider documentation for API changes
- Review OAuth app settings
- Verify backend token validation logic
- Contact development team for support
