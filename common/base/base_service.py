from typing import TypeVar, Generic, List, Optional, Any, Dict
from common.base.base_repository import BaseRepository

T = TypeVar('T')


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.repository.find_by_id(entity_id)

    def get_all(self, filters: Optional[Dict[str, Any]] = None, order_by: Optional[str] = None,
                order_desc: bool = True, page: int = 1, limit: int = 10) -> List[T]:
        return self.repository.find_all(filters, order_by, order_desc, page, limit)

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        return self.repository.count(filters)

    def create(self, entity: T) -> T:
        return self.repository.create(entity)

    def create_many(self, entities: List[T]) -> List[T]:
        return self.repository.create_many(entities)

    def update(self, entity: T) -> T:
        return self.repository.update(entity)

    def delete(self, entity_id: int, deleted_by_user_id: Optional[int] = None) -> bool:
        return self.repository.soft_delete(entity_id, deleted_by_user_id)
