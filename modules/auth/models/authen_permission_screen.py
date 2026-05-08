from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class AuthenPermissionScreen(BaseModel):
    __tablename__ = 'authen_permission_screen'

    code = mapped_column(VARCHAR(50))
    name = mapped_column(VARCHAR(255))
    type = mapped_column(VARCHAR(10))
    navigate = mapped_column(VARCHAR(255))
