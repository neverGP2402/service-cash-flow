from typing import Tuple


def normalize_pagination(page: int, limit: int, max_limit: int = 100) -> Tuple[int, int]:
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
    if limit > max_limit:
        limit = max_limit
    return page, limit


def calculate_total_pages(total: int, limit: int) -> int:
    return (total + limit - 1) // limit if limit > 0 else 0
