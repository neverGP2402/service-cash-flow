from datetime import datetime, timezone
from flask import jsonify, Response
from typing import Any, Optional


def error_response(message: str = 'error', status_code: int = 500, description: str = '') -> tuple:
    response = {
        'data': None,
        'message': message,
        'status': status_code,
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'description': description
    }
    return jsonify(response), status_code
