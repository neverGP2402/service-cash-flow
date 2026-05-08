from datetime import datetime
from typing import Optional
import bcrypt
from common.base.base_service import BaseService
from common.utils.jwt_util import generate_access_token, generate_refresh_token
from common.exceptions.auth_exception import InvalidCredentialsException
from modules.auth.repositories.auth_user_repository import AuthUserRepository
from modules.auth.repositories.auth_session_repository import AuthSessionRepository
from modules.auth.models.auth_users import AuthUser
from modules.auth.models.auth_sessions import AuthSession
from config.logger import get_logger

logger = get_logger(__name__)


class AuthService(BaseService):
    def __init__(self):
        self.user_repository = AuthUserRepository()
        self.session_repository = AuthSessionRepository()
        super().__init__(self.user_repository)

    def register(self, data: dict) -> AuthUser:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')

        if self.user_repository.find_by_username(username):
            raise InvalidCredentialsException(message='Username already exists')
        if self.user_repository.find_by_email(email):
            raise InvalidCredentialsException(message='Email already exists')

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = AuthUser(
            username=username,
            email=email,
            password=hashed,
            full_name=full_name,
            status='ACTIVE',
            register_date=datetime.utcnow()
        )
        return self.user_repository.create(user)

    def login(self, username: str, password: str, device_info: str = '', ip_address: str = '') -> dict:
        user = self.user_repository.find_by_username(username)
        if not user:
            raise InvalidCredentialsException(message='Invalid username or password')

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise InvalidCredentialsException(message='Invalid username or password')

        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)

        session = AuthSession(
            user_id=user.id,
            session_token=access_token,
            refresh_token=refresh_token,
            device_info=device_info,
            ip_address=ip_address,
            status='ACTIVE',
            type='SIGNIN',
            platform='WEB'
        )
        self.session_repository.create(session)

        user.last_login_time = datetime.utcnow()
        self.user_repository.update(user)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }

    def logout(self, user_id: int) -> bool:
        sessions = self.session_repository.find_by_user_id(user_id)
        for session in sessions:
            session.status = 'REVOKED'
            self.session_repository.update(session)
        return True
