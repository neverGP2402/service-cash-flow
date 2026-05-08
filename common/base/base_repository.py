from typing import TypeVar, Generic, List, Optional, Any, Dict
from sqlalchemy import desc, asc, and_
from config.database import db

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model_class: type):
        self.model_class = model_class
        self.session = db.session

    def find_by_id(self, entity_id: int) -> Optional[T]:
        return (
            self.session.query(self.model_class)
            .filter(and_(self.model_class.id == entity_id, self.model_class.is_deleted.is_(False)))
            .first()
        )

    def find_all(self, filters: Optional[Dict[str, Any]] = None, order_by: Optional[str] = None,
                 order_desc: bool = True, page: int = 1, limit: int = 10) -> List[T]:
        query = self.session.query(self.model_class).filter(self.model_class.is_deleted.is_(False))

        if filters:
            for key, value in filters.items():
                if hasattr(self.model_class, key) and value is not None:
                    query = query.filter(getattr(self.model_class, key) == value)

        if order_by and hasattr(self.model_class, order_by):
            order_func = desc if order_desc else asc
            query = query.order_by(order_func(getattr(self.model_class, order_by)))
        else:
            query = query.order_by(desc(self.model_class.created_at))

        return query.offset((page - 1) * limit).limit(limit).all()

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        query = self.session.query(self.model_class).filter(self.model_class.is_deleted.is_(False))
        if filters:
            for key, value in filters.items():
                if hasattr(self.model_class, key) and value is not None:
                    query = query.filter(getattr(self.model_class, key) == value)
        return query.count()

    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def create_many(self, entities: List[T]) -> List[T]:
        self.session.add_all(entities)
        self.session.commit()
        for entity in entities:
            self.session.refresh(entity)
        return entities

    def update(self, entity: T) -> T:
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def soft_delete(self, entity_id: int, deleted_by_user_id: Optional[int] = None) -> bool:
        entity = self.find_by_id(entity_id)
        if not entity:
            return False
        entity.is_deleted = True
        if deleted_by_user_id is not None and hasattr(entity, 'updated_by_user_id'):
            entity.updated_by_user_id = deleted_by_user_id
        self.session.commit()
        return True

    def hard_delete(self, entity: T) -> None:
        self.session.delete(entity)
        self.session.commit()
