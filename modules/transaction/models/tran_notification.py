from sqlalchemy import BigInteger, VARCHAR, DateTime, Boolean
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class TranNotification(BaseModel):
    __tablename__ = 'tran_notification'

    user_id = mapped_column(BigInteger, nullable=False)
    transaction_id = mapped_column(BigInteger)
    title = mapped_column(VARCHAR(255))
    content = mapped_column(VARCHAR(255))
    type = mapped_column(VARCHAR(20))
    status = mapped_column(VARCHAR(20))
    sent_at = mapped_column(DateTime)
    is_read = mapped_column(Boolean, default=False)
    read_at = mapped_column(DateTime)
    priority = mapped_column(VARCHAR(20))
