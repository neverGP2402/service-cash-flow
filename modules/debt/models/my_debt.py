from sqlalchemy import BigInteger, VARCHAR, DateTime, Double, Integer, JSON
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class MyDebt(BaseModel):
    __tablename__ = 'my_debt'

    user_id = mapped_column(BigInteger, nullable=False)
    contract_no = mapped_column(VARCHAR(50))
    contract_date = mapped_column(DateTime)
    counterparty_id = mapped_column(BigInteger)
    debt_type = mapped_column(VARCHAR(20))
    type = mapped_column(VARCHAR(20))
    file_path_json = mapped_column(JSON)
    frequency = mapped_column(VARCHAR(20))
    principal_debt = mapped_column(Double, default=0)
    interest = mapped_column(Double, default=0)
    interest_rate = mapped_column(Double, default=0)
    insurance_fee = mapped_column(Double, default=0)
    into_money = mapped_column(Double, default=0)
    paid_amount = mapped_column(Double, default=0)
    remaining_amount = mapped_column(Double, default=0)
    cycle = mapped_column(Integer)
    paymented_times = mapped_column(Integer)
    start_date = mapped_column(DateTime)
    exp_date = mapped_column(DateTime)
    status = mapped_column(VARCHAR(20))
    description = mapped_column(VARCHAR(255))
