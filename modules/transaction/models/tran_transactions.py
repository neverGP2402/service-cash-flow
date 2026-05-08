from sqlalchemy import BigInteger, VARCHAR, DateTime, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class TranTransaction(BaseModel):
    __tablename__ = 'tran_transactions'

    user_id = mapped_column(BigInteger, nullable=False)
    type = mapped_column(VARCHAR(50))
    category_id = mapped_column(BigInteger)
    bill_image = mapped_column(VARCHAR(255))
    amount = mapped_column(Double, nullable=False, default=0)
    date = mapped_column(DateTime)
    status = mapped_column(VARCHAR(50))
    formality_transaction = mapped_column(VARCHAR(50))
    wallet_id = mapped_column(BigInteger)
    origin_transaction_id = mapped_column(BigInteger)
    description = mapped_column(VARCHAR(255))
    reference = mapped_column(VARCHAR(255))
    meta_data = mapped_column(VARCHAR(255))
