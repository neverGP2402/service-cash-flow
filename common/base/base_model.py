from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer
from sqlalchemy.orm import mapped_column
from config.database import db


class BaseModel(db.Model):
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_deleted = mapped_column(Boolean, default=False, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by_user_id = mapped_column(BigInteger, nullable=True)
    updated_by_user_id = mapped_column(BigInteger, nullable=True)

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat() if value else None
            else:
                result[column.name] = value
        return result
