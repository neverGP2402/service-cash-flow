from sqlalchemy import BigInteger, VARCHAR, DateTime, Double, Integer
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class MyDebtDetail(BaseModel):
    __tablename__ = 'my_debt_detail'

    my_debt_id = mapped_column(BigInteger, nullable=False)
    principal_debt = mapped_column(Double, default=0)
    interest = mapped_column(Double, default=0)
    insurance_fee = mapped_column(Double, default=0)
    into_money = mapped_column(Double, default=0)
    paid_amount = mapped_column(Double, default=0)
    remaining_amount = mapped_column(Double, default=0)
    payment_times = mapped_column(Integer)
    payment_date = mapped_column(DateTime)
    payment_method = mapped_column(VARCHAR(50))
    transaction_id = mapped_column(BigInteger)
    wallet_id = mapped_column(BigInteger)
    bill_id = mapped_column(BigInteger)
    status = mapped_column(VARCHAR(20))
    description = mapped_column(VARCHAR(255))
