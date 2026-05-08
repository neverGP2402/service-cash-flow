from flask import Flask, request, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from common.exceptions.auth_exception import UnauthorizedException
from config.logger import get_logger

logger = get_logger(__name__)


def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()
            g.current_user_id = int(identity) if identity else None
        except Exception as e:
            logger.error(f"JWT verification failed: {str(e)}")
            raise UnauthorizedException(description=str(e))
        return fn(*args, **kwargs)
    return wrapper


def get_current_user_id() -> int:
    return getattr(g, 'current_user_id', None)


def register_auth_middleware(app: Flask):
    @app.before_request
    def load_user():
        excluded_paths = ['/health', '/api/v1/auth/login', '/api/v1/auth/register',
                          '/api/v1/auth/refresh', '/api/v1/auth/forgot-password']
        if request.path in excluded_paths or request.path.endswith('/health'):
            return
