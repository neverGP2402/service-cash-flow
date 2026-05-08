from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class AuthenPermissionScreenRole(BaseModel):
    __tablename__ = 'authen_permission_screen_role'

    permission_screen_id = mapped_column(BigInteger, nullable=False)
    permission_id = mapped_column(BigInteger, nullable=False)
