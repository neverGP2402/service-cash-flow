from flask import Flask
from common.responses.error_response import error_response
from config.logger import get_logger

logger = get_logger(__name__)


class AppException(Exception):
    def __init__(self, message: str = 'Application error', status_code: int = 500, description: str = ''):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.description = description


class NotFoundException(AppException):
    def __init__(self, message: str = 'Resource not found', description: str = ''):
        super().__init__(message, 404, description)


class BadRequestException(AppException):
    def __init__(self, message: str = 'Bad request', description: str = ''):
        super().__init__(message, 400, description)


class UnauthorizedException(AppException):
    def __init__(self, message: str = 'Unauthorized', description: str = ''):
        super().__init__(message, 401, description)


class ForbiddenException(AppException):
    def __init__(self, message: str = 'Forbidden', description: str = ''):
        super().__init__(message, 403, description)


def register_error_handlers(app: Flask):
    @app.errorhandler(AppException)
    def handle_app_exception(e: AppException):
        if e.status_code >= 500:
            logger.error(f"AppException: {e.message} | {e.description}", exc_info=True)
        return error_response(message=e.message, status_code=e.status_code, description=e.description)

    @app.errorhandler(404)
    def handle_404(e):
        return error_response(message='Not found', status_code=404, description=str(e))

    @app.errorhandler(405)
    def handle_405(e):
        return error_response(message='Method not allowed', status_code=405, description=str(e))

    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return error_response(message='Internal server error', status_code=500, description=str(e))
