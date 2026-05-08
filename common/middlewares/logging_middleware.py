from flask import Flask, request, g
from config.logger import get_logger
import time

logger = get_logger(__name__)


def register_logging_middleware(app: Flask):
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        duration = (time.time() - getattr(g, 'start_time', time.time())) * 1000
        logger.info(
            f"{request.method} {request.path} - {response.status_code} - {duration:.2f}ms"
        )
        return response
