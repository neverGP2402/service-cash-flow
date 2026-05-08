from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Boolean, DateTime, String, Text, Float, Integer, JSON
from sqlalchemy.orm import declared_attr, mapped_column
from datetime import datetime


db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


class BaseColumnMixin:
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    is_deleted = mapped_column(Boolean, default=False, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by_user_id = mapped_column(BigInteger, nullable=True)
    updated_by_user_id = mapped_column(BigInteger, nullable=True)
