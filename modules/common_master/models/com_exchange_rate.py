from sqlalchemy import BigInteger, VARCHAR, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class ComExchangeRate(BaseModel):
    __tablename__ = 'com_exchange_rate'

    exchange_rate_purchase = mapped_column(Double, default=0)
    exchange_rate_sell = mapped_column(Double, default=0)
    asset_id = mapped_column(BigInteger)
    description = mapped_column(VARCHAR(255))
    origin_info = mapped_column(VARCHAR(255))
