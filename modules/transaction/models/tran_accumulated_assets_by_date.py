from sqlalchemy import BigInteger, VARCHAR, DateTime, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class TranAccumulatedAssetsByDate(BaseModel):
    __tablename__ = 'tran_accumulated_assets_by_date'

    user_id = mapped_column(BigInteger, nullable=False)
    asset_id = mapped_column(BigInteger)
    unit_id = mapped_column(BigInteger)
    value_remaining = mapped_column(Double, default=0)
    description = mapped_column(VARCHAR(255))
    date = mapped_column(DateTime)
