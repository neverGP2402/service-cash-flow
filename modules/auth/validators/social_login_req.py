from common.exceptions.validate_exception import ValidationException
from common.utils.validate_util import require_field


class SocialLoginReq:
    def __init__(self, data: dict):
        self.provider = require_field(data, 'provider')
        self.access_token = require_field(data, 'access_token')
        self.email = data.get('email', '')
        self.name = data.get('name', '')
        self.avatar = data.get('avatar', '')
        self.device_info = data.get('device_info', '')
        # Bỏ ip_address - backend sẽ tự detect
        
        # Validate provider
        self._validate_provider()
    
    def _validate_provider(self):
        """Validate OAuth provider"""
        valid_providers = ['google', 'github', 'facebook']
        if self.provider.lower() not in valid_providers:
            raise ValidationException(f"Provider must be one of: {', '.join(valid_providers)}")
        self.provider = self.provider.lower()
    
    def to_dict(self):
        """Convert to dictionary for service layer"""
        return {
            'provider': self.provider,
            'access_token': self.access_token,
            'email': self.email,
            'name': self.name,
            'avatar': self.avatar,
            'device_info': self.device_info
            # ip_address sẽ được backend tự detect
        }
