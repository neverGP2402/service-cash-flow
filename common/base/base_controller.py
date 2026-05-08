from typing import Any, Dict, List, Optional
from flask import request
from common.responses.success_response import success_response, paginated_response
from common.responses.error_response import error_response


class BaseController:
    def _get_current_user_id(self) -> Optional[int]:
        from flask_jwt_extended import get_jwt_identity
        identity = get_jwt_identity()
        if identity:
            return int(identity)
        return None

    def _get_pagination_params(self) -> Dict[str, int]:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:
            limit = 10
        return {'page': page, 'limit': limit}

    def _get_filter_params(self, allowed_fields: List[str]) -> Dict[str, Any]:
        filters = {}
        for field in allowed_fields:
            value = request.args.get(field)
            if value is not None:
                filters[field] = value
        return filters

    def ok(self, data: Any = None, message: str = 'success', description: str = ''):
        return success_response(data=data, message=message, description=description)

    def created(self, data: Any = None, message: str = 'created', description: str = ''):
        return success_response(data=data, message=message, status_code=201, description=description)

    def paginated(self, data: List[Any], page: int, limit: int, total: int, message: str = 'success',
                  description: str = ''):
        return paginated_response(data=data, page=page, limit=limit, total=total, message=message,
                                   description=description)

    def bad_request(self, message: str = 'bad request', description: str = ''):
        return error_response(message=message, status_code=400, description=description)

    def not_found(self, message: str = 'not found', description: str = ''):
        return error_response(message=message, status_code=404, description=description)

    def unauthorized(self, message: str = 'unauthorized', description: str = ''):
        return error_response(message=message, status_code=401, description=description)

    def forbidden(self, message: str = 'forbidden', description: str = ''):
        return error_response(message=message, status_code=403, description=description)

    def internal_error(self, message: str = 'internal server error', description: str = ''):
        return error_response(message=message, status_code=500, description=description)
