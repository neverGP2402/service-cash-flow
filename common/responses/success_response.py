from datetime import datetime, timezone
from flask import jsonify
from typing import Any, Dict, List, Optional


def success_response(data: Any = None, message: str = 'success', status_code: int = 200,
                     description: str = '') -> tuple:
    response = {
        'data': data if data is not None else {},
        'message': message,
        'status': status_code,
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'description': description
    }
    return jsonify(response), status_code


def paginated_response(data: List[Any], page: int, limit: int, total: int,
                       message: str = 'success', description: str = '') -> tuple:
    total_pages = (total + limit - 1) // limit if limit > 0 else 0
    response = {
        'data': {
            'data': data if data is not None else [],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'totalPages': total_pages
            }
        },
        'message': message,
        'status': 200,
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'description': description
    }
    return jsonify(response), 200
