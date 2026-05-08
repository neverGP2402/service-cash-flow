from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class AuthPermission(BaseModel):
    __tablename__ = 'auth_permission'

    code = mapped_column(VARCHAR(50))
    name = mapped_column(VARCHAR(100))
    description = mapped_column(VARCHAR(255))
