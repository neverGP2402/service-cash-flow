from sqlalchemy import BigInteger, VARCHAR, DateTime, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class MyExpense(BaseModel):
    __tablename__ = 'my_expense'

    user_id = mapped_column(BigInteger, nullable=False)
    expense_id = mapped_column(BigInteger)
    type = mapped_column(VARCHAR(20))
    frequency = mapped_column(VARCHAR(20))
    amount = mapped_column(Double, default=0)
    price = mapped_column(Double, default=0)
    into_money = mapped_column(Double, default=0)
    effective_date = mapped_column(DateTime)
    exp_date = mapped_column(DateTime)
    status = mapped_column(VARCHAR(20))
    description = mapped_column(VARCHAR(255))
