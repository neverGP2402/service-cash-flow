from sqlalchemy import BigInteger, VARCHAR, DateTime, Integer
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class AuthUser(BaseModel):
    __tablename__ = 'auth_users'

    username = mapped_column(VARCHAR(100))
    password = mapped_column(VARCHAR(255))
    full_name = mapped_column(VARCHAR(255))
    avatar = mapped_column(VARCHAR(255))
    birthday = mapped_column(DateTime)
    age = mapped_column(Integer)
    register_date = mapped_column(DateTime)
    gender = mapped_column(VARCHAR(10))
    province_id = mapped_column(BigInteger)
    ward_id = mapped_column(BigInteger)
    address = mapped_column(VARCHAR(255))
    email = mapped_column(VARCHAR(255))
    status = mapped_column(VARCHAR(50))
    role_permission_id = mapped_column(BigInteger)
    last_login_time = mapped_column(DateTime)
    last_request_time = mapped_column(DateTime)
