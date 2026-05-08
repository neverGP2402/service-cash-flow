from sqlalchemy import BigInteger, VARCHAR, DateTime, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class MyTargetPlan(BaseModel):
    __tablename__ = 'my_target_plan'

    user_id = mapped_column(BigInteger, nullable=False)
    target_id = mapped_column(BigInteger, nullable=False)
    income = mapped_column(Double, default=0)
    expense = mapped_column(Double, default=0)
    into_money_actual = mapped_column(Double, default=0)
    date = mapped_column(DateTime)
    status = mapped_column(VARCHAR(20))
