from sqlalchemy import BigInteger, VARCHAR, DateTime
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class AuthSession(BaseModel):
    __tablename__ = 'auth_sessions'

    user_id = mapped_column(BigInteger, nullable=False)
    session_token = mapped_column(VARCHAR(255))
    expires_at = mapped_column(DateTime)
    refresh_token = mapped_column(VARCHAR(255))
    refresh_token_expires_at = mapped_column(DateTime)
    refresh_token_used = mapped_column(VARCHAR(255))
    last_request_time = mapped_column(DateTime)
    device_info = mapped_column(VARCHAR(255))
    ip_address = mapped_column(VARCHAR(255))
    status = mapped_column(VARCHAR(50))
    type = mapped_column(VARCHAR(10))
    platform = mapped_column(VARCHAR(50))
