from flask import Flask, request
from config.logger import get_logger

logger = get_logger(__name__)


def register_request_middleware(app: Flask):
    @app.before_request
    def before_request():
        if request.is_json:
            logger.debug(f"Request JSON: {request.get_json(silent=True)}")
