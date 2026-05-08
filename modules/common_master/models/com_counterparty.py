from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class ComCounterparty(BaseModel):
    __tablename__ = 'com_counterparty'

    code = mapped_column(VARCHAR(50))
    name = mapped_column(VARCHAR(255))
    phone = mapped_column(VARCHAR(20))
    avatar = mapped_column(VARCHAR(255))
