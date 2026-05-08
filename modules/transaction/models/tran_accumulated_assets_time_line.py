from sqlalchemy import BigInteger, VARCHAR, Double
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class TranAccumulatedAssetsTimeLine(BaseModel):
    __tablename__ = 'tran_accumulated_assets_time_line'

    user_id = mapped_column(BigInteger, nullable=False)
    transaction_id = mapped_column(BigInteger)
    asset_id = mapped_column(BigInteger)
    unit_id = mapped_column(BigInteger)
    value_remaining = mapped_column(Double, default=0)
    description = mapped_column(VARCHAR(255))
