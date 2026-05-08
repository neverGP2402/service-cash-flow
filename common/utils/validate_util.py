from typing import Any, List, Optional


def require_field(data: dict, field: str) -> Any:
    value = data.get(field)
    if value is None or (isinstance(value, str) and value.strip() == ''):
        raise ValueError(f"Field '{field}' is required")
    return value


def require_fields(data: dict, fields: List[str]) -> List[Any]:
    results = []
    for field in fields:
        results.append(require_field(data, field))
    return results


def to_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
