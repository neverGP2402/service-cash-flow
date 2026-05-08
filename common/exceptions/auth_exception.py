from common.exceptions.app_exception import AppException


class AuthException(AppException):
    def __init__(self, message: str = 'Authentication error', status_code: int = 401, description: str = ''):
        super().__init__(message, status_code, description)


class TokenExpiredException(AuthException):
    def __init__(self, message: str = 'Token has expired', description: str = ''):
        super().__init__(message, 401, description)


class InvalidTokenException(AuthException):
    def __init__(self, message: str = 'Invalid token', description: str = ''):
        super().__init__(message, 401, description)


class InvalidCredentialsException(AuthException):
    def __init__(self, message: str = 'Invalid credentials', description: str = ''):
        super().__init__(message, 401, description)


class UnauthorizedException(AuthException):
    def __init__(self, message: str = 'Unauthorized', description: str = ''):
        super().__init__(message, 401, description)
