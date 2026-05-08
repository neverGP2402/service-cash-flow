from sqlalchemy import BigInteger, VARCHAR, DateTime, Double, Integer
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class TranResultByMonth(BaseModel):
    __tablename__ = 'tran_result_by_month'

    user_id = mapped_column(BigInteger, nullable=False)
    unit_id = mapped_column(BigInteger)
    income = mapped_column(Double, default=0)
    expense = mapped_column(Double, default=0)
    accumulated_income = mapped_column(Double, default=0)
    accumulated_expense = mapped_column(Double, default=0)
    change_income_month_one_before = mapped_column(Double, default=0)
    change_expense_month_one_before = mapped_column(Double, default=0)
    type = mapped_column(VARCHAR(20))
    month = mapped_column(Integer)
    year = mapped_column(Integer)
    month_before = mapped_column(Integer)
    year_before = mapped_column(Integer)
    description = mapped_column(VARCHAR(255))
    date = mapped_column(DateTime)
