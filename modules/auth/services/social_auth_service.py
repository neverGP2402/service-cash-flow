import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
from common.base.base_service import BaseService
from common.utils.jwt_util import generate_access_token, generate_refresh_token
from common.exceptions.auth_exception import InvalidCredentialsException
from modules.auth.repositories.auth_user_repository import AuthUserRepository
from modules.auth.repositories.auth_session_repository import AuthSessionRepository
from modules.auth.models.auth_users import AuthUser
from modules.auth.models.auth_sessions import AuthSession
from config.logger import get_logger

logger = get_logger(__name__)


class SocialAuthService(BaseService):
    def __init__(self):
        self.user_repository = AuthUserRepository()
        self.session_repository = AuthSessionRepository()
        super().__init__(self.user_repository)
    
    def login_with_social(self, data: dict) -> dict:
        """Login with OAuth provider"""
        provider = data.get('provider')
        access_token = data.get('access_token')
        
        # Verify token with provider
        user_info = self._verify_social_token(provider, access_token)
        
        if not user_info:
            raise InvalidCredentialsException(message='Invalid social token')
        
        # Find or create user
        user = self._find_or_create_user(provider, user_info, data)
        
        # Create session
        session_data = self._create_session(user, data)
        
        # Update user login time
        user.last_login_time = datetime.utcnow()
        self.user_repository.update(user)
        
        return {
            'access_token': session_data['access_token'],
            'refresh_token': session_data['refresh_token'],
            'user': user.to_dict(),
            'is_new_user': not bool(self.user_repository.find_by_email(user_info.get('email')))
        }
    
    def _verify_social_token(self, provider: str, access_token: str) -> Optional[Dict[str, Any]]:
        """Verify OAuth token with provider"""
        try:
            if provider == 'google':
                return self._verify_google_token(access_token)
            elif provider == 'github':
                return self._verify_github_token(access_token)
            elif provider == 'facebook':
                return self._verify_facebook_token(access_token)
        except Exception as e:
            logger.error(f"Social token verification failed for {provider}: {e}")
            return None
    
    def _verify_google_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Verify Google OAuth token"""
        url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        return {
            'id': data.get('id'),
            'email': data.get('email'),
            'name': data.get('name'),
            'avatar': data.get('picture'),
            'verified': data.get('verified_email', False)
        }
    
    def _verify_github_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Verify GitHub OAuth token"""
        headers = {'Authorization': f'token {access_token}'}
        
        # Get user info
        user_response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        if user_response.status_code != 200:
            return None
        
        user_data = user_response.json()
        
        # Get user emails (GitHub requires separate API call for emails)
        emails_response = requests.get('https://api.github.com/user/emails', headers=headers, timeout=10)
        emails_data = emails_response.json() if emails_response.status_code == 200 else []
        
        # Find primary verified email
        primary_email = None
        for email_info in emails_data:
            if email_info.get('verified', False) and email_info.get('primary', False):
                primary_email = email_info.get('email')
                break
        
        if not primary_email:
            primary_email = user_data.get('email')  # Fallback
        
        return {
            'id': user_data.get('id'),
            'email': primary_email,
            'name': user_data.get('name'),
            'avatar': user_data.get('avatar_url'),
            'username': user_data.get('login'),
            'verified': bool(primary_email)
        }
    
    def _verify_facebook_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Verify Facebook OAuth token"""
        url = f"https://graph.facebook.com/me?fields=id,name,email,picture&access_token={access_token}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        # Get avatar URL
        avatar_url = None
        if 'picture' in data and 'data' in data['picture']:
            avatar_url = data['picture']['data'].get('url')
        
        return {
            'id': data.get('id'),
            'email': data.get('email'),
            'name': data.get('name'),
            'avatar': avatar_url,
            'verified': bool(data.get('email'))
        }
    
    def _find_or_create_user(self, provider: str, user_info: Dict[str, Any], request_data: dict) -> AuthUser:
        """Find existing user or create new one"""
        email = user_info.get('email')
        
        # Case 1: Email không có từ provider
        if not email:
            raise InvalidCredentialsException(
                message='Email is required from social provider. Please grant email permission.',
                error_code='EMAIL_REQUIRED'
            )
        
        # Case 2: Email chưa được verified
        if not user_info.get('verified', False):
            raise InvalidCredentialsException(
                message='Email address is not verified. Please verify your email with the provider first.',
                error_code='EMAIL_NOT_VERIFIED'
            )
        
        # Find user by email
        user = self.user_repository.find_by_email(email)
        
        if user:
            # Case 3: User đã tồn tại - cập nhật info và return
            self._update_user_social_info(user, provider, user_info)
            return user
        
        # Case 4: User chưa tồn tại - tạo mới
        return self._create_user_from_social(provider, user_info)
    
    def _update_user_social_info(self, user: AuthUser, provider: str, user_info: Dict[str, Any]):
        """Update existing user with social info"""
        updated = False
        
        if not user.avatar and user_info.get('avatar'):
            user.avatar = user_info['avatar']
            updated = True
        
        if not user.full_name and user_info.get('name'):
            user.full_name = user_info['name']
            updated = True
        
        if updated:
            self.user_repository.update(user)
    
    def _create_user_from_social(self, provider: str, user_info: Dict[str, Any]) -> AuthUser:
        """Create new user from social login"""
        # Generate unique username
        base_username = user_info.get('username', user_info.get('email', '').split('@')[0])
        username = self._generate_unique_username(base_username)
        
        user = AuthUser(
            username=username,
            email=user_info['email'],
            password='',  # No password for social users
            full_name=user_info.get('name', ''),
            avatar=user_info.get('avatar', ''),
            status='ACTIVE',
            register_date=datetime.utcnow()
        )
        
        return self.user_repository.create(user)
    
    def _generate_unique_username(self, base_username: str) -> str:
        """Generate unique username from base"""
        username = base_username.lower().replace(' ', '_')
        counter = 1
        
        while self.user_repository.find_by_username(username):
            username = f"{base_username.lower().replace(' ', '_')}_{counter}"
            counter += 1
        
        return username
    
    def _create_session(self, user: AuthUser, request_data: dict) -> Dict[str, str]:
        """Create session for user"""
        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)
        
        session = AuthSession(
            user_id=user.id,
            session_token=access_token,
            refresh_token=refresh_token,
            device_info=request_data.get('device_info', ''),
            ip_address=request_data.get('ip_address', ''),
            status='ACTIVE',
            type='SIGNIN',
            platform='WEB'
        )
        
        self.session_repository.create(session)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
