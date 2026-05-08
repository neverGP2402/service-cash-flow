from sqlalchemy import BigInteger, VARCHAR
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class ComAsset(BaseModel):
    __tablename__ = 'com_asset'

    code = mapped_column(VARCHAR(50))
    name = mapped_column(VARCHAR(255))
    type = mapped_column(VARCHAR(10))
    unit_id = mapped_column(BigInteger)
