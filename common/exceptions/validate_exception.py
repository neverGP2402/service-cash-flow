from common.exceptions.app_exception import AppException


class ValidationException(AppException):
    def __init__(self, message: str = 'Validation error', description: str = '', errors: dict = None):
        super().__init__(message, 400, description)
        self.errors = errors or {}
