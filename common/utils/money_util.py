from typing import Optional


def round_money(value: Optional[float], decimals: int = 2) -> Optional[float]:
    if value is None:
        return None
    return round(float(value), decimals)


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default
