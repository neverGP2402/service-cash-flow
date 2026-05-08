from sqlalchemy import BigInteger, VARCHAR, DateTime, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class TranTransactionDetail(BaseModel):
    __tablename__ = 'tran_transactions_detail'

    transaction_id = mapped_column(BigInteger, nullable=False)
    user_id = mapped_column(BigInteger, nullable=False)
    product_name = mapped_column(VARCHAR(255))
    amount = mapped_column(Double, default=0)
    price = mapped_column(Double, default=0)
    into_money = mapped_column(Double, default=0)
    date = mapped_column(DateTime)
    description = mapped_column(VARCHAR(255))
