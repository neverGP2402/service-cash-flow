from datetime import datetime, timezone
from typing import Optional


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        value = value.replace('Z', '+00:00')
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def format_iso(dt: Optional[datetime]) -> Optional[str]:
    if not dt:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat().replace('+00:00', 'Z')


def get_month_range(year: int, month: int):
    from calendar import monthrange
    start = datetime(year, month, 1, 0, 0, 0)
    last_day = monthrange(year, month)[1]
    end = datetime(year, month, last_day, 23, 59, 59)
    return start, end
