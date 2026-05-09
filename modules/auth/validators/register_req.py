from common.exceptions.validate_exception import ValidationException
from common.utils.validate_util import require_field
import re
from datetime import datetime


class RegisterReq:
    def __init__(self, data: dict):
        # Required fields
        self.username = require_field(data, 'username')
        self.email = require_field(data, 'email')
        self.password = require_field(data, 'password')
        
        # Optional fields with defaults
        self.full_name = data.get('full_name', '').strip()
        self.avatar = data.get('avatar', '').strip()
        self.birthday = self._parse_date(data.get('birthday'))
        self.age = self._calculate_age(self.birthday)
        self.gender = self._validate_gender(data.get('gender'))
        self.province_id = self._parse_int(data.get('province_id'))
        self.ward_id = self._parse_int(data.get('ward_id'))
        self.address = data.get('address', '').strip()
        self.role_permission_id = self._parse_int(data.get('role_permission_id'))
        
        # Validate required fields
        self._validate_username()
        self._validate_email()
        self._validate_password()
        self._validate_full_name()
    
    def _parse_date(self, date_str):
        """Parse date string to datetime object"""
        if not date_str:
            return None
        try:
            # Support multiple date formats
            formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            raise ValidationException("Invalid date format. Use YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY")
        except Exception:
            raise ValidationException("Invalid date format")
    
    def _calculate_age(self, birthday):
        """Calculate age from birthday"""
        if not birthday:
            return None
        today = datetime.now()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        return age
    
    def _validate_gender(self, gender):
        """Validate gender field"""
        if not gender:
            return None
        valid_genders = ['MALE', 'FEMALE', 'OTHER']
        gender = gender.upper().strip()
        if gender not in valid_genders:
            raise ValidationException(f"Gender must be one of: {', '.join(valid_genders)}")
        return gender
    
    def _parse_int(self, value):
        """Parse integer value"""
        if not value:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValidationException("Invalid integer value")
    
    def _validate_username(self):
        """Validate username"""
        if len(self.username) < 3:
            raise ValidationException("Username must be at least 3 characters long")
        if len(self.username) > 50:
            raise ValidationException("Username must be less than 50 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', self.username):
            raise ValidationException("Username can only contain letters, numbers, and underscores")
    
    def _validate_email(self):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValidationException("Invalid email format")
        if len(self.email) > 255:
            raise ValidationException("Email must be less than 255 characters")
    
    def _validate_password(self):
        """Validate password strength"""
        if len(self.password) < 8:
            raise ValidationException("Password must be at least 8 characters long")
        if len(self.password) > 255:
            raise ValidationException("Password must be less than 255 characters")
        
        # Check for at least one uppercase, one lowercase, one digit
        if not re.search(r'[A-Z]', self.password):
            raise ValidationException("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', self.password):
            raise ValidationException("Password must contain at least one lowercase letter")
        if not re.search(r'\d', self.password):
            raise ValidationException("Password must contain at least one digit")
    
    def _validate_full_name(self):
        """Validate full name"""
        if self.full_name and len(self.full_name) > 255:
            raise ValidationException("Full name must be less than 255 characters")
        if self.full_name and not re.match(r'^[a-zA-Z\s\u00C0-\u00FF]+$', self.full_name):
            raise ValidationException("Full name can only contain letters and spaces")
    
    def to_dict(self):
        """Convert to dictionary for database insertion"""
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,  # Will be hashed in service layer
            'full_name': self.full_name,
            'avatar': self.avatar,
            'birthday': self.birthday,
            'age': self.age,
            'gender': self.gender,
            'province_id': self.province_id,
            'ward_id': self.ward_id,
            'address': self.address,
            'role_permission_id': self.role_permission_id
        }
