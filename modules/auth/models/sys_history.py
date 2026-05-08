from sqlalchemy import BigInteger, VARCHAR, Text, DateTime, JSON
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class SysHistory(BaseModel):
    __tablename__ = 'sys_history'

    user_id = mapped_column(BigInteger, nullable=True)
    process_id = mapped_column(BigInteger, nullable=True)
    session_id = mapped_column(BigInteger, nullable=True)
    description = mapped_column(VARCHAR(255))
    method = mapped_column(VARCHAR(10))
    api_path = mapped_column(VARCHAR(255))
    param = mapped_column(JSON)
    status = mapped_column(VARCHAR(10))
    start_request_time = mapped_column(DateTime)
    finish_request_time = mapped_column(DateTime)
    message_response = mapped_column(Text)
