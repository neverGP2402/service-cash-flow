from sqlalchemy import BigInteger, VARCHAR, DateTime, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class MyTarget(BaseModel):
    __tablename__ = 'my_target'

    user_id = mapped_column(BigInteger, nullable=False)
    name = mapped_column(VARCHAR(255))
    income = mapped_column(Double, default=0)
    expense = mapped_column(Double, default=0)
    description = mapped_column(VARCHAR(255))
    time_cycle = mapped_column(Double, default=0)
    type = mapped_column(VARCHAR(20))
    progress = mapped_column(Double, default=0)
    status = mapped_column(VARCHAR(20))
    setting_date = mapped_column(DateTime)
    effective_date = mapped_column(DateTime)
