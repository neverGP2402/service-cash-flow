from sqlalchemy import BigInteger, VARCHAR, DateTime, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class MyInfoAsset(BaseModel):
    __tablename__ = 'my_info_asset'

    user_id = mapped_column(BigInteger, nullable=False)
    asset_id = mapped_column(BigInteger)
    wallet_id = mapped_column(BigInteger)
    amount = mapped_column(Double, default=0)
    price = mapped_column(Double, default=0)
    origin = mapped_column(VARCHAR(255))
    status = mapped_column(VARCHAR(20))
    description = mapped_column(VARCHAR(255))
    unit_id = mapped_column(BigInteger)
    transaction_date = mapped_column(DateTime)
